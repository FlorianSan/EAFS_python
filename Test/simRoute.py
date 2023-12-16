import ivy
import time
from ivy.std_api import *


IVYAPPNAME = 'simRoute'
readymsg = '%s is ready' % IVYAPPNAME

ivybus = ''


def on_connection_change(agent, event):
    pass


def on_die(agent, _id):
    IvyStop()


# initialising the bus
IvyInit(IVYAPPNAME,  # application name for Ivy
        readymsg,  # ready message
        0,  # parameter ignored
        on_connection_change,  # handler called on connection/disconnection
        on_die)  # handler called when a die msg is received

# starting the bus
IvyStart(ivybus)

time.sleep(2)
IvySendMsg('FR_Ready Time=147.4 Initial Flight Plan Ready')
time.sleep(1)
IvySendMsg('FR_InitFlightPlan Time=155.29999999999998 FROM=LFBO TO=LFPO ROUTE=DIRECT-FISTO, UY156-PERIG, UT210-TUDRA, UT158-BEVOL, DIRECT-STAR')