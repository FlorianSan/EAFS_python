#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ivy.std_api import *

#Envoie le AP_STATE et AP_MODE à l'EFIS
def sendBA_OBJ(time, baObj):
    print("Send ba obj : "+str(baObj))
    IvySendMsg("GC;BA_OBJ;TIME="+str(time)+";BA_OBJ="+str(baObj))