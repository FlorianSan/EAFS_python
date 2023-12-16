import DatabaseException
import DatabaseManager


class IhmManager:
    def __init__(self, FPLN_Route, FPLN_Leg, FPLN_temporary, _communicationManager):
        self.flightPlanRoute = FPLN_Route
        self.flightPlanLeg = FPLN_Leg
        self.flightPlanTemporary = FPLN_temporary
        self.communicationManager = _communicationManager
        pass

    def run(self):
        while True:
            print("1 - Afficher ListLeg")
            print("2 - Afficher Route")
            print("3 - Modifier Leg")
            choice = input()
            if choice == "1":
                self.AfficherListLeg()
            elif choice == "2":
                self.AfficherRoute()
            elif choice == "3":
                self.ModifyMenu()
            else:
                print("Entrée non valide")

    def AfficherListLeg(self):
        self.flightPlanLeg.afficher()
        pass

    def AfficherRoute(self):
        self.flightPlanRoute.afficher()
        pass

    def ModifyMenu(self):
        print("0 - Retour au menu principal")
        print("1 - Insertion")
        print("2 - Suppression")
        print("3 - Modification")
        choice = input()
        if choice == "0":
            pass
        elif choice == "1":
            self.insertLeg()
        elif choice == "2":
            self.deleteLeg()
        elif choice == "3":
            self.modifLeg()
        else:
            print("Entrée non valide")
        pass

    def modifLeg(self):
        print("Entrer le numéro de séquence du leg à modifier")
        seq = int(input())
        if seq >= len(self.flightPlanLeg.listLegs) or seq < 0:
            print("séquence non valide")
        # insertion avant la leg active
        elif seq <= self.flightPlanLeg.activeLeg.seq:
            print("Vous ne pouvez effectuer une modification sur le leg active ou les legs précédentes")
        else:
            print("1 - Flyby \n2 - Flyover")
            choice = input()
            if choice == "1":
                self.flightPlanLeg.listLegs[seq].waypoint.type = "Flyby"
            elif choice == "2":
                self.flightPlanLeg.listLegs[seq].waypoint.type = "Flyover"
            else:
                print("Entrée non valide")
            self.communicationManager.sendLegList()

    def insertLeg(self):
        print("Entrer le numéro de séquence du leg précédent l'insertion")
        seq = int(input())
        print("Entrer le WPT à inserer")
        WPT = input()

        try:
            # vérification de l'existance du waypoint
            databaseManager = DatabaseManager.Database_Manager()
            databaseManager.loadWpt(WPT)
            databaseManager.close_connection()

            # insertion au dela de la liste de leg
            if seq >= len(self.flightPlanLeg.listLegs) or seq < 0:
                print("séquence d'insertion non valide")
            # insertion avant la leg active
            elif seq <= self.flightPlanLeg.activeLeg.seq:
                print("Vous ne pouvez effectuer une modification sur le leg active ou les legs précédentes")
            else:
                preLeg = self.flightPlanLeg.listLegs[seq]
                postLeg = self.flightPlanLeg.listLegs[seq + 1]

                # Insertion d'un wpt entre deux sections de route
                if preLeg.routeSeq != postLeg.routeSeq:
                    preAwy = self.flightPlanRoute.listRoute[preLeg.routeSeq]
                    newSegment = preAwy[0] + "-" + preAwy[1] + ", DIRECT-" + WPT + ", DIRECT-" + postLeg.waypoint.id
                    self.modificationRoute(preLeg.routeSeq, preLeg.routeSeq, newSegment)
                # Insertion d'un wpt au sein d'une section de route(AWY)
                elif preLeg.routeSeq == postLeg.routeSeq:
                    Awy, WptEndAwy = self.flightPlanRoute.listRoute[preLeg.routeSeq][0], \
                        self.flightPlanRoute.listRoute[preLeg.routeSeq][1]
                    # on insère un waypoint juste avant le dernier waypoint de l'awy
                    if WptEndAwy == postLeg.waypoint.id:
                        newSegment = Awy + "-" + preLeg.waypoint.id + ", " + "DIRECT-" + WPT + ", DIRECT-" + postLeg.waypoint.id
                    else:
                        newSegment = Awy + "-" + preLeg.waypoint.id + ", " + "DIRECT-" + WPT + ", DIRECT-" + postLeg.waypoint.id + ", " + Awy + "-" + WptEndAwy
                    self.modificationRoute(preLeg.routeSeq, preLeg.routeSeq, newSegment)

        except DatabaseException.DatabaseNotFoundException as exc:
            print(exc)
        pass

    def deleteLeg(self):
        print("Entrer le numéro de séquence du leg à supprimer")
        seq = int(input())

        # si aéroport de départ
        if seq == 0:
            print("Vous ne pouvez pas supprimer l'aéroport de départ")
        # Si suppression avant la leg active
        elif seq <= self.flightPlanLeg.activeLeg.seq:
            print("Vous ne pouvez effectuer une modification sur le leg active ou les précédentes")
        # si aéroport d'arrivée
        elif seq == len(self.flightPlanLeg.listLegs) - 1:
            print("Vous ne pouvez pas supprimer l'aéroport d'arrivée")
        elif seq >= len(self.flightPlanLeg.listLegs) or seq < 1:
            print("séquence d'insertion non valide")
        else:
            # Si un direct
            Leg = self.flightPlanLeg.listLegs[seq]
            routeSection = self.flightPlanRoute.listRoute[Leg.routeSeq]
            if routeSection[0] == "DIRECT":
                postLeg = self.flightPlanLeg.listLegs[seq + 1]
                postRouteSection = self.flightPlanRoute.listRoute[postLeg.routeSeq]
                # La section suivante est un Direct
                if postRouteSection[0] == "DIRECT":
                    newSegment = postRouteSection[0] + "-" + postRouteSection[1]
                    self.modificationRoute(Leg.routeSeq, postLeg.routeSeq, newSegment)
                # La section suivante est une Airways
                else:
                    newSegment = "DIRECT-" + postLeg.waypoint.id + ", " + postRouteSection[0] + "-" + postRouteSection[
                        1]
                    self.modificationRoute(Leg.routeSeq, postLeg.routeSeq, newSegment)
            # Si au sein d'une airways
            else:
                preLeg = self.flightPlanLeg.listLegs[seq - 1]
                postLeg = self.flightPlanLeg.listLegs[seq + 1]
                Awy, WptEndAwy = self.flightPlanRoute.listRoute[Leg.routeSeq][0], \
                    self.flightPlanRoute.listRoute[Leg.routeSeq][1]
                # Si wpt de fin d'awy
                if routeSection[1] == Leg.waypoint.id:
                    print("suppression du wpt de fin d'AWY")
                    newSegment = Awy + "-" + preLeg.waypoint.id + ", DIRECT-" + postLeg.waypoint.id
                    self.modificationRoute(Leg.routeSeq, Leg.routeSeq, newSegment)
                # si wpt avant dernier d'une airway ET 2e wpt d'une airways
                elif routeSection[1] == postLeg.waypoint.id and preLeg.routeSeq != Leg.routeSeq:
                    print("suppression du 2e wpt d'une section d'awy de 3 wpt")
                    newSegment = "DIRECT-" + postLeg.waypoint.id
                    self.modificationRoute(Leg.routeSeq, Leg.routeSeq, newSegment)
                # si wpt avant dernier d'une airway
                elif routeSection[1] == postLeg.waypoint.id:
                    print("suppression avant dernier d'une airways")
                    newSegment = Awy + "-" + preLeg.waypoint.id + ", DIRECT-" + postLeg.waypoint.id
                    self.modificationRoute(Leg.routeSeq, Leg.routeSeq, newSegment)
                # si 2e wpt d'une airways
                elif preLeg.routeSeq != Leg.routeSeq:
                    print("suppression du 2e wpt d'une airways")
                    newSegment = "DIRECT-" + postLeg.waypoint.id + ", " + Awy + "-" + WptEndAwy
                    self.modificationRoute(Leg.routeSeq, Leg.routeSeq, newSegment)
                # si autre
                else:
                    print("suppression au sein d'une airways")
                    newSegment = Awy + "-" + preLeg.waypoint.id + ", DIRECT-" + postLeg.waypoint.id + ", " + Awy + "-" + WptEndAwy
                    self.modificationRoute(Leg.routeSeq, Leg.routeSeq, newSegment)

    def modificationRoute(self, changeRouteSeqStart, changeRouteSeqEnd, modifiedSegment):

        newSegment = modifiedSegment.split(", ")
        for i in range(len(newSegment)):
            routeidentifiant = newSegment[i].split("-")[0]
            fixidentifiant = newSegment[i].split("-")[1]
            newSegment[i] = (routeidentifiant, fixidentifiant)

        # copie de la liste de legs vers le flight plan temporaire
        self.flightPlanTemporary.listLegs = self.flightPlanLeg.listLegs

        # Effectuer la modification sur la route
        self.flightPlanRoute.change(changeRouteSeqStart, changeRouteSeqEnd, newSegment)

        # Effectuer le changement sur la liste de legs
        self.flightPlanTemporary.change(changeRouteSeqStart, changeRouteSeqEnd, newSegment)

        # Echange du fpln temporaire et du fpln actif
        self.flightPlanLeg.listLegs = self.flightPlanTemporary.listLegs

        # Envoi de la leg List au module TRAJ
        self.communicationManager.sendLegList()

        # Envoi de la route modifiée au module Route
        self.communicationManager.commModificationToRoute(changeRouteSeqStart, changeRouteSeqEnd, modifiedSegment)
