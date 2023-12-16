# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from ivy.std_api import *
import time
import threading
import DatabaseException


class CommunicationManager:

    def __init__(self, _FPLN_Route, _FPLN_Leg, _FPLN_temporary):
        IvyInit("FPLN_APP_LEGS", "Ready", 0)
        IvyStart("")

        self.TIME = 0.0
        self.endprog = True
        self.recept = False

        self.flightPlanRoute = _FPLN_Route
        self.flightPlanLeg = _FPLN_Leg
        self.flightPlanTemporary = _FPLN_temporary

        self.modifiedRouteMessage = ""  # Besoin de conserver ce message en cas de mauvaise réception de route

        IvyBindMsg(self.initReady, "FR_Ready Time=(.*) Initial Flight Plan Ready")
        IvyBindMsg(self.initFlightPlan, "FR_InitFlightPlan Time=(.*) FROM=(.*) TO=(.*) ROUTE=(.*)")
        IvyBindMsg(self.sequencing, "GS_AL Time=(.*) NumSeqActiveLeg=(.*)")
        IvyBindMsg(self.errorTransmissionTraj, "GT_ERROR Time=(.*) Error Receiving Flight Plan")
        IvyBindMsg(self.horloge, "Time t=(.*)")
        IvyBindMsg(self.modifReady, "FR_ModifReady Time=(.*) Modified Flight Plan Ready")
        IvyBindMsg(self.modificationRoute, "FR_Modif Time=(.*) numStart=(.*) numEnd=(.*) ModifiedSection=(.*)")
        IvyBindMsg(self.sendModifRouteAfterError, "FR_ERROR Time=(.*) Error Receiving Modified Route")

    # Lance le communication manager
    def run(self):
        IvyMainLoop()

    # Receptionne le message d'horloge de la simulation
    def horloge(self, agent, *larg):
        self.TIME = float(larg[0])
        pass

    # Chronomètre de s secondes pour gérer les messages de non réception
    def chrono(self, s):
        time.sleep(s)
        self.endprog = False

    # Validation de la réception d'un message
    def reception(self, commType):
        while self.endprog and not self.recept:
            print("attente")
            time.sleep(1)
        if not self.recept:
            if commType == "modif":
                IvySendMsg("FL_ERROR Time={} Error Receiving Modification".format(self.TIME))
            elif commType == "init":
                IvySendMsg("FL_ERROR Time={} Error Receiving Flight Plan".format(self.TIME))
            print("la transmission a échouée")
        pass

    # reception du message de prévention d'envoi du message d'initialisation
    def initReady(self, agent, *larg):
        self.recept = False
        self.endprog = True
        print("Prêt à recevoir")
        t1 = threading.Thread(target=self.chrono, args=(7,))
        t2 = threading.Thread(target=self.reception, args=("init",))
        t1.start()
        t2.start()
        pass

    # Reception du message de prévention d'envoi du message de modification
    def modifReady(self, agent, *larg):
        self.recept = False
        self.endprog = True
        print("Prêt à recevoir modif")
        t1 = threading.Thread(target=self.chrono, args=(7,))
        t2 = threading.Thread(target=self.reception, args=("modif",))
        t1.start()
        t2.start()
        pass

    # reception du message d'initialisation de la route et du flight plan
    def initFlightPlan(self, agent, *larg):
        self.recept = True
        try:
            self.flightPlanRoute.initRoute(larg[1], larg[2], larg[3])
            self.flightPlanLeg.initFPLN(self.flightPlanRoute)
            message = "FL_LegList Time=" + str(self.TIME) + " LegList=(" + self.flightPlanLeg.LongTermList() + ")"
            print(message)
            IvySendMsg(message)
            IvySendMsg("FL_START_FLIGHT")

        except DatabaseException.DatabaseNotFoundException as exc:
            print(exc)
        pass

    # reception du message de séquencement (leg active)
    def sequencing(self, agent, *larg):
        NumSeqActiveLeg = int(larg[1])
        activeLeg = self.flightPlanLeg.listLegs[NumSeqActiveLeg]
        self.flightPlanLeg.activeLeg = activeLeg
        # legMessage = "FL_LegList Time=" + str(self.TIME) + " LegList=(" + self.flightPlanLeg.LongTermList() + ")"
        # print(legMessage)
        # IvySendMsg(legMessage)

        messageActiveLeg = activeLeg.message()
        print(messageActiveLeg)

        activeRouteSeq = activeLeg.routeSeq
        ActiveAwyMessage = "FL_AA Time=" + str(self.TIME) + " NumActiveAwy=" + str(activeRouteSeq)
        IvySendMsg(ActiveAwyMessage)
        print(ActiveAwyMessage)

        # Afficher la liste des legs
        self.flightPlanLeg.afficher()

    # réception du message d'erreur de reception du module TRAJ et renvoie de la list de leg
    def errorTransmissionTraj(self, agent, *larg):
        message = "FL_LegList Time=" + str(self.TIME) + " LegList=(" + self.flightPlanLeg.LongTermList() + ")"
        IvySendMsg(message)
        print(message)

    # réception et traitement d'une modification du module ROUTE
    def modificationRoute(self, agent, *larg):
        self.recept = True

        changeRouteSeqStart = int(larg[1])
        changeRouteSeqEnd = int(larg[2])

        newSegment = larg[3].split(", ")
        for i in range(len(newSegment)):
            routeidentifiant = newSegment[i].split("-")[0]
            fixidentifiant = newSegment[i].split("-")[1]
            newSegment[i] = (routeidentifiant, fixidentifiant)

        # copie de la liste de legs vers le flight plan temporaire
        self.flightPlanTemporary.listLegs = self.flightPlanLeg.listLegs

        # Disjonction de cas en fonction de s'il s'agit d'une insertion ou un changement d'un ou plusieur segment
        if self.flightPlanRoute.listRoute[changeRouteSeqStart] == newSegment[0]:  # insertion
            # Effectuer la modification sur la route
            self.flightPlanRoute.change(changeRouteSeqStart, changeRouteSeqEnd, newSegment)
            # Effectuer le changement sur la liste de legs
            self.flightPlanTemporary.change(changeRouteSeqStart + 1, changeRouteSeqEnd, newSegment[1:])
        else:
            # Effectuer la modification sur la route
            self.flightPlanRoute.change(changeRouteSeqStart, changeRouteSeqEnd, newSegment)
            # Effectuer le changement sur la liste de legs
            self.flightPlanTemporary.change(changeRouteSeqStart, changeRouteSeqEnd, newSegment)

        # Echange du fpln temporaire et du fpln actif
        self.flightPlanLeg.listLegs = self.flightPlanTemporary.listLegs
        self.flightPlanLeg.listLegs = self.flightPlanTemporary.listLegs

        # Envoi de la leg List au groupe TRAJ
        message = "FL_LegList Time=" + str(self.TIME) + " LegList=(" + self.flightPlanLeg.LongTermList() + ")"
        print(message)
        IvySendMsg(message)

    # Envoi de la route modifiée au module ROUTE
    def commModificationToRoute(self, seqStart, seqEnd, newSegment):
        IvySendMsg("FL_ModifReady Modified Flight Plan Ready")
        message = "FL_Modif Time=" + str(self.TIME) + " numStart=" + str(seqStart) + " numEnd=" + str(
            seqEnd) + " modifiedSection=" + newSegment
        IvySendMsg(message)
        self.modifiedRouteMessage = message
        pass

    # Renvoi de la route modifiée en cas de non réception
    def sendModifRouteAfterError(self):
        IvySendMsg(self.modifiedRouteMessage)
        pass

    # Envoi de la liste de leg au module TRAJ et SEQ
    def sendLegList(self):
        message = "FL_LegList Time=" + str(self.TIME) + " LegList=(" + self.flightPlanLeg.LongTermList() + ")"
        print(message)
        IvySendMsg(message)
        pass
