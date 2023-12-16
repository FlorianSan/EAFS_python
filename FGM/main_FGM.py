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
          "time": 0,
          "baObjFMM": 0,
          "hdgObj": 0,
          "trkObj": 0,
          "APMode": 0}

Datas = {"roll": 0,
         "fpa": 0,
         "hdg": 0,
         "vp": 0,
         "time": 0,
         "baObjFMM": 0,
         "hdgObj": 0,
         "trkObj": 0,
         "APMode": "Managed"}

mutexRoll = mutexFpa = mutexHdg = mutexVp = mutexGS = Lock()
mutexTime = mutexAPMode = mutexBaObjFMM = mutexHdgObj = mutexStatut = Lock()
listApMode = ["Managed", "SelectedHeading"]
in_test = False
statut = "deactivated"

global startedFlight


def run(test_mode=0):
    global statut
    statut = "activated"
    bus = IvyInit("FGM_APP", "Hello from FGM_APP", 0)
    IvyStart()
    bind()


def reboot(who):
    global rebootNb
    print(who)
    if rebootNb < 3:
        IvyStop()
        os.execv("/usr/bin/python3", (os.getcwd(), sys.argv[0], str(rebootNb + 1)))
    else:
        print("arret du prgm")
        sys.exit()


# Bind les messages Ivy aux fonctions
def bind():
    IvyBindMsg(getBA_OBJ, "^GC;BA_OBJ;TIME=(.*);BA_OBJ=(.*)")
    IvyBindMsg(getPosition,
               "^AircraftSetPosition X=(.*) Y=(.*) Altitude-ft=(.*) Roll=(.*) Pitch=(.*) Yaw=(.*) Heading=(.*) Airspeed=(.*) Groundspeed=(.*)")
    IvyBindMsg(getState, "^StateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)")
    IvyBindMsg(getCDUMode, "^FCULateral Mode=(.*) Val=(.*)")
    IvyBindMsg(startFlight, "^InitStateVector.*")
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


# Recoit le mode de l'AP et le heading objectif (=-1 si en managed) depuis le module CDU
def getCDUMode(self, *arg):
    global States, Datas
    if in_test: print("getCDUMode", arg)

    mutexAPMode.acquire()
    if not testError(arg[0], "ap_mode", "APMode"):
        Datas["APMode"] = arg[0]
        States["APMode"] = 1
    mutexAPMode.release()

    mutexHdgObj.acquire()
    if not testError(arg[1], "float", "hdgObj"):
        Datas["hdgObj"] = float(arg[1])
        States["hdgObj"] = 1
    mutexHdgObj.release()


# Recoit le bank angle objectif du module FMM GUID-COMM
def getBA_OBJ(self, *arg):
    global States, Datas
    if in_test: print("getBA_OBJ", arg)

    mutexBaObjFMM.acquire()
    if not testError(arg[1], "float", "baObjFMM"):
        Datas["baObjFMM"] = float(arg[1])
        States["baObjFMM"] = 1
    mutexBaObjFMM.release()


# Recoit le time et calcule et envoit la commande de roulis et les facteurs de charges nx et nz au modèle
def clock(self, *arg):
    global States, Datas
    if in_test: print("clock", arg)
    if startedFlight == 1:

        mutexTime.acquire()
        Datas["time"] = arg[0]
        mutexTime.release()

        # On travaille ici avec des variables locales pour des raisons de prog concurrente
        localRoll = localFpa = localHdg = localTAS = localBaObjFMM = localBaObj = localAPMode = None

        mutexRoll.acquire()
        localRoll = Datas["roll"]
        States["roll"] -= 1
        mutexRoll.release()
        # if States["roll"]<-2 : reboot("roll")

        mutexFpa.acquire()
        localFpa = Datas["fpa"]
        States["fpa"] -= 1
        mutexFpa.release()
        # if States["fpa"]<-2 : reboot("fpa")

        mutexHdg.acquire()
        localHdg = Datas["hdg"]
        States["hdg"] -= 1
        mutexHdg.release()
        # if States["hdg"]<-2 : reboot("hdg")

        mutexVp.acquire()
        localVp = Datas["vp"]
        States["vp"] -= 1
        mutexVp.release()
        # if States["vp"]<-2 : reboot("vp")

        mutexAPMode.acquire()
        localAPMode = Datas["APMode"]
        States["APMode"] -= 1
        mutexAPMode.release()
        # if States["APMode"]<-2 : reboot("APMode")

        # Calcul du roll angle objectif en mode Selected
        if localAPMode == "SelectedHeading":
            print("selected")
            mutexHdgObj.acquire()
            localHdgObj = Datas["hdgObj"]
            States["hdgObj"] -= 1
            mutexHdgObj.release()
            # if States["hdgObj"]<-2 : reboot("hdgObj")

            localBaObj = computeBA_OBJ(localRoll, localFpa, localHdg, localVp, localHdgObj)

        # Verification du roll angle objectif calculé par le FMM en mode Managed et calcul de l'heading correspondant
        elif localAPMode == "Managed":
            print("managed")
            mutexBaObjFMM.acquire()
            localBaObjFMM = Datas["baObjFMM"]
            States["baObjFMM"] -= 1
            mutexBaObjFMM.release()
            # if States["baObjFMM"]<-2 : reboot("baObjFMM")

            localBaObj = checkValidityBaFMM(localBaObjFMM)

            localHdgObj = computeTRK_OBJ(localRoll, localFpa, localHdg, localVp, localBaObj)

        # Calcul du roll rate et des facteurs de charges pour obtenir le roll angle objectif
        p, nx, nz = computeCommand(localRoll, localFpa, localBaObj)

        # Envoi des commandes au modèle
        sendRollRate(p)
        sendNx(nx)
        sendNz(nz)

        # Envoi des données aux EFIS
        sendAP_STATE(Datas["time"], statut, localAPMode)
        sendBA_OBJ(Datas["time"], localBaObj)
        sendTRK_OBJ(Datas["time"], localHdgObj)


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
