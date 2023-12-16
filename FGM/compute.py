#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constant import *
from math import *

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def computeBA_OBJ(roll,fpa,hdg,Vp,hdgObj):
    print("HDG : ",hdg, "HDG voulu : ", hdgObj)
    nz = cos(fpa)/cos(roll)
    k4 = Vp/(G*nz*TAU_PSI)
    errorHeading = (hdgObj-hdg)*PI/180
    if errorHeading > PI :
        return(clamp(k4*(errorHeading-2*PI),-PI/3,PI/3))
    elif errorHeading < -PI :
        return(clamp(k4*(2*PI-errorHeading),-PI/3,PI/3))
    else :
        return(clamp(k4*errorHeading,-PI/3,PI/3))
    

def computeTRK_OBJ(roll,fpa,hdg,Vp,baObj):
    nz = cos(fpa)/cos(roll)
    if Vp != 0 :
        return(hdg+TAU_PSI*G*nz*baObj/Vp)
    else:
        return(hdg)

def checkValidityBaFMM(localBaObjFMM):
    return(clamp(localBaObjFMM,-PI/3,PI/3))

def computeCommand(roll,fpa,baObj):
    print(roll, fpa, baObj)
    k1 = 1/TAU_PHI
    p = clamp(k1*(baObj-roll),-PI/30,PI/30)
    nx = clamp(sin(fpa),-1.5,1.5)
    nz = clamp(cos(fpa)/cos(roll),-1.5,1.5)
    return(p,nx,nz)