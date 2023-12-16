from ivy.std_api import *
import time

IvyInit("TEST_APP", "Bonjour de TEST_APP")
IvyStart() # mettre 'bus' entre parenthèse si utilisation du wifi
time.sleep(1.0)  # attente du temps de l'initialisation

def sendNoError():
    IvySendMsg("GC;BA_OBJ;TIME=1;BA_OBJ=1")
    IvySendMsg("^AircraftSetPosition X=1 Y=1 Altitude-ft=1 Roll=1 Pitch=1 Yaw=1 Heading=1 Airspeed=1 Groundspeed=1")
    IvySendMsg("^StateVector x=1y=1 z=1 Vp=1 fpa=1 psi=1 phi=1")
    IvySendMsg("FCULateral Mode=Managed Val=0")
    #IvySendMsg("InitStateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)")
    IvySendMsg("Time t=1")

def sendOneError():
    #IvySendMsg("GC;BA_OBJ;TIME=1;BA_OBJ=1")
    IvySendMsg("^AircraftSetPosition X=1 Y=1 Altitude-ft=1 Roll=1 Pitch=1 Yaw=1 Heading=1 Airspeed=1 Groundspeed=1")
    IvySendMsg("^StateVector x=1y=1 z=1 Vp=1 fpa=1 psi=1 phi=1")
    IvySendMsg("FCULateral Mode=Managed Val=0")
    #IvySendMsg("InitStateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)")
    IvySendMsg("Time t=1")

sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)

sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)

sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)

sendNoError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendNoError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendNoError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)
sendOneError()
time.sleep(1.0)