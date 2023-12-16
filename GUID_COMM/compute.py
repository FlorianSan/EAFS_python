#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constant import *
from math import *

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
   
def computeBA_OBJ(roll,fpa,gs,Vp,TAE,XTK):
    print(roll,fpa,gs,Vp,TAE,XTK)
    
    nz = cos(fpa)/cos(roll)
    k2 = -Vp/(G*nz*TAU_PSI)
    if gs != 0 :
        k3 = -Vp/(G*nz*gs*TAU_XTK*TAU_PSI)
    else:
        k3=0
    return(clamp(k2*TAE+k3*XTK,-PI/3,PI/3))