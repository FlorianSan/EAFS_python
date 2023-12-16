#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from ivy.std_api import *
from threading import Thread, Lock
from send import *
from compute import *
from constant import *

States = {"roll": 0,
          "fpa": 0,
          "hdg": 0,
          "vp": 0,
          "gs": 0,
          "time": 0,
          "TAE": 0,
          "XTK": 0}
Datas = {"roll": 0,
         "fpa": 0,
         "hdg": 0,
         "vp": 0,
         "gs": 0,
         "time": 0,
         "TAE": 0,
         "XTK": 0}

mutexRoll = mutexFpa = mutexHdg = mutexVp = mutexGS = mutexTAE = mutexXTK = Lock()
mutexTime = mutexBaObjFMM = mutexStatut = Lock()
in_test = False

statut = "deactivated"
global startedFlight


def run(test_mode=0):
    global statut
    statut = "activated"
    bus = IvyInit("GUID_COMM_APP", "Hello from GUID_COMM_APP", 0)
    IvyStart()
    bind()


def reboot():
    global rebootNb
    if rebootNb < 3:
        IvyStop()
        os.execv("/usr/bin/python3", (os.getcwd(), sys.argv[0], str(rebootNb + 1)))
    else:
        print("arret du prgm")
        sys.exit()


# Bind les messages Ivy aux fonctions
def bind():
    IvyBindMsg(getPosition,
               "^AircraftSetPosition X=(.*) Y=(.*) Altitude-ft=(.*) Roll=(.*) Pitch=(.*) Yaw=(.*) Heading=(.*) Airspeed=(.*) Groundspeed=(.*)")
    IvyBindMsg(getTrackError, "^GS_Data Time=(.*) XTK=(.*) TAE=(.*) DTWPT=(.*) BANK_ANGLE_REF=(.*) ALDTWPT=(.*)")
    IvyBindMsg(startFlight, "^InitStateVector.*")
    IvyBindMsg(getState, "^StateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)")
    IvyBindMsg(clock, "^Time t=(.*)")
    IvyMainLoop()


def getState(*arg):
    global States, Datas
    if in_test: print("getState", arg)
    mutexRoll.acquire()
    if not testError(arg[7], "float", "roll"):
        Datas["roll"] = float(arg[7])
        States["roll"] = 1
    mutexRoll.release()

    mutexFpa.acquire()
    if not testError(arg[5], "float", "fpa"):
        Datas["fpa"] = float(arg[5])
        States["fpa"] = 1
    mutexFpa.release()

    mutexVp.acquire()
    if not testError(arg[4], "float", "vp"):
        Datas["vp"] = float(arg[4])
        States["vp"] = 1
    mutexVp.release()


# Recoit les données du modèle (position, angles, vitesses...)
def getPosition(*arg):
    global States, Datas
    if in_test: print("getPos", arg)

    mutexHdg.acquire()
    if not testError(arg[7], "float", "hdg"):
        Datas["hdg"] = float(arg[7])
        States["hdg"] = 1
    mutexHdg.release()

    mutexGS.acquire()
    if not testError(arg[9], "float", "gs"):
        Datas["gs"] = float(arg[9])
        States["gs"] = 1
    mutexGS.release()


# Recoit le XTK et TAE du module FMM GUID-
def getTrackError(self, *arg):
    global States, Datas
    if in_test: print("getTrackError", arg)

    mutexXTK.acquire()
    if not testError(arg[1], "float", "XTK"):
        Datas["XTK"] = float(arg[1]) * NMTOM
        States["XTK"] = 1
    mutexXTK.release()

    mutexTAE.acquire()
    if not testError(arg[2], "float", "TAE"):
        Datas["TAE"] = float(arg[2])
        States["TAE"] = 1
    mutexTAE.release()


# Recoit le time et calcule et envoit la commande de roulis et les facteurs de charges nx et nz au modèle
def clock(self, *arg):
    global States, Datas
    if in_test: print("clock", arg)
    if startedFlight == 1:
        mutexTime.acquire()
        Datas["time"] = arg[0]
        mutexTime.release()

        # On travaille ici avec des variables locales pour des raisons de prog concurrente
        localRoll = localFpa = localGS = localVp = localTAE = localXTK = 0

        mutexRoll.acquire()
        localRoll = Datas["roll"]
        States["roll"] -= 1
        mutexRoll.release()
        # if States["roll"]<-2 : reboot()

        mutexFpa.acquire()
        localFpa = Datas["fpa"]
        States["fpa"] -= 1
        mutexFpa.release()
        # if States["fpa"]<-2 : reboot()

        mutexGS.acquire()
        localGS = Datas["gs"]
        States["gs"] -= 1
        mutexGS.release()
        # if States["gs"]<-2 : reboot()

        mutexVp.acquire()
        localVp = Datas["vp"]
        States["vp"] -= 1
        mutexVp.release()
        # if States["vp"]<-2 : reboot()

        mutexTAE.acquire()
        localTAE = Datas["TAE"]
        States["TAE"] -= 1
        mutexTAE.release()
        # if States["TAE"]<-2 : reboot()

        mutexXTK.acquire()
        localXTK = Datas["XTK"]
        States["XTK"] -= 1
        mutexXTK.release()
        # if States["XTK"]<-2 : reboot()

        # Calcul du roll angle objectif
        baObjFMM = computeBA_OBJ(localRoll, localFpa, localGS, localVp, localTAE, localXTK)
        # Envoi le bank angle objectif au FGM
        IvySendMsg("GC;BA_OBJ;TIME=" + str(Datas["time"]) + ";BA_OBJ=" + str(baObjFMM))


def testError(value, typeData, state):
    global States, Datas
    isError = False

    # Verifier si la donnee est presente
    if (value == "") or (value == ''):
        isError = True
    else:
        if (typeData == "ap_mode"):
            if value not in listApMode:
                isError = True

        # Verifier le type de la donnee
        if typeData == "float":
            try:
                value = float(value)
            except:
                isError = True

    return (isError)


def startFlight(*arg):

    print("flight started")
    startedFlight = 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        rebootNb = int(sys.argv[1])
        if rebootNb > 0:
            startedFlight = 1
        else:
            startedFlight = 0
    else:
        rebootNb = 0
    print("Reboot : " + str(rebootNb))
    run()
