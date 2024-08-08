"""
This python file presents a simulation environment. The code will send the necessary information
on the Ivy bus in order to well communicate with the other modules and detect any problem about some
modules.
"""

from ivy.std_api import *
import time


class Environment():

    def __init__(self):
        self.busInit()
        # print('info sent')
        # IvyBindMsg(self.getFpln_route,'^(.*)')
        # IvyBindMsg(self.getFpln_route,'FR_Ready Time=(.*) Initial Flight Plan Ready')
        IvyBindMsg(self.getFpln_route,"^FR_InitFlightPlan Time=(.*) FROM=(.*) TO=(.*) ROUTE=(.*)")
        # IvyBindMsg(self.getFpln_route(), "GS_AL Time=(.*) NumSeqActiveLeg=(.*)")
        IvyBindMsg(self.getPosition,"^InitStateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*) AircraftSetPosition X=(.*) Y=(.*) Altitude-ft=(.*) Roll=(.*) Pitch=(.*) Yaw=(.*) Heading=(.*) Airspeed=(.*) Groundspeed=(.*)")
        # IvyBindMsg(self.getPosition,".*")
        # self.busSend()
        appList = self.busInfo()
        print(appList)


    # Bus initialization
    def busInit(self):
        """
        This function implementation initializes the ivy bus. The purpose is to prepare the bus to
        a goog communication between modules.
        :return: bus initialized
        """
        IvyInit("Simulation environment")
        IvyStart()
        time.sleep(1)
        self.busInfo()

    # Send Info
    def busSend(self):
        """
        This function send some information to the other modules like the Flight Plan Route
        :return: A boolean to know if info have been sent.
        """
        t = time.localtime()
        current_time = time.strftime("%S",t)
        # print(current_time)
        dep_apt = 'LFBO' # departure airport
        arr_apt = 'LFPO' # arrival airport
        route = 'DIRECT-FISTO, UY156-PERIG, UT210-TUDRA, UT158-AMB, DIRECT-STAR'  # route that the A/C will follow
        # IvySendMsg('FR_Ready Time={} Initial Flight Plan Ready'.format(current_time))

        IvySendMsg('FR_Ready Time='+str(current_time)+' Initial Flight Plan Ready')
        time.sleep(2)
        IvySendMsg('FR_InitFlightPlan Time=155.29999999999998 FROM=LFBO TO=LFPO ROUTE=DIRECT-FISTO, UY156-PERIG, UT210-TUDRA, UT158-AMB, DIRECT-STAR')
        time.sleep(2)

    # Receive Info
    def busRecv(self):
        """
        This function receive some information from the others modules like the Flight Plan Route
        :return: Information received.
        """
        pass

    # Run other modules in order to test the simulation
    # def run(self):
    #     send
    #     testIvySIMU
    #     testFGM
    #     testIvySEQ
    #     testIvyLEGS
    #     send_msg

    def msgBind(self,*arg):
        print("Time msg on the bus : %r",arg)
        # print("Agent %r used time"%agent)

    def getPosition(self,*arg): print(arg)

    def getFpln_route(self,*arg): print(arg)

    # Have some info about modules connected on the bus
    def busInfo(self):
        """
        This function allows us to have some information about agents (modules) connected to the bus
        for example the list of these modules connected and some specific information about a module.
        :return: Agent connected
        """
        return IvyGetApplicationList()




if __name__ == "__main__":

    Environment()


