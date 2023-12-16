#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ivy.std_api import *

#Envoie le roll rate p au modele et les facteurs de charges nx et nz
def sendRollRate(p):
    print("Send roll", p)
    IvySendMsg("APLatControl rollRate="+str(p))

#Envoie le facteurs de charges nx au modele
def sendNx(nx):
    print("Send nx", nx)
    IvySendMsg("APNxControl nx="+str(nx))

#Envoie le facteurs de charges nz au modele
def sendNz(nz):
    print("Send nz", nz)
    IvySendMsg("APNzControl nz="+str(nz))

#Envoie le AP_STATE et AP_MODE à l'EFIS
def sendAP_STATE(time,state,mode):
    IvySendMsg("FG;AP_STATE;TIME="+str(time)+";AP_STATE="+str(state)+" AP_MODE"+str(mode))

#Envoie le BA_OBJ à l'EFIS
def sendBA_OBJ(time,ba_obj):
    IvySendMsg("FG;BA_OBJ;TIME="+str(time)+";BA_OBJ="+str(ba_obj))

#Envoie le TRK_OBJ à l'EFIS
def sendTRK_OBJ(time,trk_obj):
    IvySendMsg("FG;TRK_OBJ;TIME="+str(time)+";TRK_OBJ="+str(trk_obj))
