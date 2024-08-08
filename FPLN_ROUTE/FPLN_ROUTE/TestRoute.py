"""
This file tests the flight plan route module. It will send the flight plan on the bus
"""

"""
Classes and functions table
"""

from ivy.std_api import *
import time
from FPLN_ROUTE.Model.Airport import Airport
from FPLN_ROUTE.Model.Fpln import Fpln

class FplnRoute:

    def __init__(self):

        self.fpln = Fpln()   # a flight plan object

        bus = "192.168.43.255:2010"

        # Initialisation
        IvyInit("ROUTE")
        IvyStart()

        time.sleep(2)

        self.setdepApt()
        self.setarrApt()
        self.setroute()
        self.print()
        self.sendFpln()


    def setdepApt(self):
        """
        Set the departure airport
        """
        depapt = str(input("Enter the departure airport\n"))
        if self.fpln.setAirportDep(identifier=depapt):
            print("Value entered")

    def setarrApt(self):
        """
        Set the arrival airport
        """
        arrapt = str(input("Enter the arrival airport\n"))
        if self.fpln.setAirportArr(identifier=arrapt):
            print("Value entered")


    def setroute(self):
        """
        Set the route
        """
        _route = str(input("Enter the route\n"))
        self.fpln.setRoute(_route)


    def sendFpln(self):
        """
        Send the flight plan
        """

        print("Ready to send...")
        t = time.localtime()
        current_time = time.strftime("%S", t)

        IvySendMsg("FR_Ready Time=" + str(current_time) + " Initial Flight Plan Ready")
        time.sleep(2)

        IvySendMsg("FR_InitFlightPlan Time=" + str(current_time) + " FROM=" + str(self.fpln.airportDep.getIdentifier()) + " TO=" + str(
        self.fpln.airportArr.getIdentifier()) + " ROUTE=" + str(self.fpln.route))
        time.sleep(2)

        print("Flight plan sent!!!")

        IvyMainLoop()

    def print(self):
        print(self.fpln.getAirportDep().identifier)
        print(self.fpln.getAirportArr().identifier)
        print(self.fpln.getRoute())
        # IvyBindMsg(self.getFpln_route, "^FR_InitFlightPlan Time=(.*) FROM=(.*) TO=(.*) ROUTE=(.*)")

    def getFpln_route(self, *arg):
        print(arg)


if __name__ == '__main__':
    """
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("ROUTE", "Bonjour du simulateur")
    IvyStart()

    time.sleep(2)

    # ****************************************************

    # Mettre plus haut (avant l'envoi des données de trajectoire
    t = time.localtime()
    current_time = time.strftime("%S", t)
    # print(current_time)
    dep_apt = 'LFBO'  # departure airport
    arr_apt = 'LFPO'  # arrival airport
    route = 'DIRECT-FISTO, UY156-PERIG, UT210-TUDRA, UT158-AMB, DIRECT-STAR'  # route that the A/C will follow
    # IvySendMsg('FR_Ready Time={} Initial Flight Plan Ready'.format(current_time))

    IvySendMsg("FR_Ready Time=" + str(current_time) + " Initial Flight Plan Ready")
    time.sleep(1)

    IvySendMsg("FR_InitFlightPlan Time=" + str(current_time) + " FROM=" + str(dep_apt) + " TO=" + str(
        arr_apt) + " ROUTE=" + str(route))
    time.sleep(1)

    # IvySendMsg("Hello data=" + str(2))
    print("message sent!!")

    # *********************************************************

    IvyMainLoop()
"""
    FplnRoute()
