import Waypoint
import Leg
import DatabaseManager


class FlightPlan:
    def __init__(self):
        self.seqNum = 0  # Pointeur pour ajouter des legs dans la table.
        self.listLegs = []
        self.activeLeg = None

    def initFPLN(self, Route):
        self.listLegs = []
        self.addDeparture(Route.departure)
        for i in range(len(Route.listRoute)):
            couple = Route.listRoute[i]
            if couple[0] == 'DIRECT':
                if couple[1] == 'STAR':
                    self.addArrival(Route.arrival, i, len(self.listLegs))
                else:
                    self.addDirect(couple[1], i, len(self.listLegs))
            else:
                self.addAirway(couple[0], couple[1], i, len(self.listLegs))

        self.activeLeg = self.listLegs[0]

    def addDeparture(self, idAirport):
        databaseManager = DatabaseManager.Database_Manager()
        latitude, longitude = databaseManager.loadAirport(idAirport)
        databaseManager.close_connection()
        AirportWpt = Waypoint.Waypoint(idAirport, latitude, longitude)
        leg = Leg.IFLeg(AirportWpt)
        self.listLegs.append(leg)
        self.seqNum = 1
        pass

    def addArrival(self, idAirport, routeSeq, seq):
        databaseManager = DatabaseManager.Database_Manager()
        latitude, longitude = databaseManager.loadAirport(idAirport)
        databaseManager.close_connection()
        AirportWpt = Waypoint.Waypoint(idAirport, latitude, longitude)
        WptFrom = self.listLegs[seq - 1].waypoint
        minaltitude = "FL000"
        maxaltitude = "FL195"
        leg = Leg.TFLeg(WptFrom, AirportWpt, seq, minaltitude, maxaltitude, routeSeq)
        self.listLegs.insert(seq, leg)
        self.seqNum += 1
        pass

    def addDirect(self, idWptTo, routeSeq, seq):
        databaseManager = DatabaseManager.Database_Manager()
        WptFrom = self.listLegs[seq - 1].waypoint
        WptTo = databaseManager.loadWpt(idWptTo)
        databaseManager.close_connection()
        minaltitude = "FL000"
        maxaltitude = "FL195"
        leg = Leg.TFLeg(WptFrom, WptTo, seq, minaltitude, maxaltitude, routeSeq)
        self.listLegs.insert(seq, leg)
        seq += 1
        return seq

    def addAirway(self, routeidentifier, fixidentifier, routeSeq, seq):
        databaseManager = DatabaseManager.Database_Manager()
        seqNumEntryWpt, EntryWpt = databaseManager.loadEntryWpt(routeidentifier, self.listLegs[seq - 1].waypoint)
        seqNumExitWpt, idExitWpt = databaseManager.loadExitWpt(routeidentifier, fixidentifier)
        awy = databaseManager.loadAwy(routeidentifier, seqNumEntryWpt, seqNumExitWpt)
        wpt1 = EntryWpt
        for i in range(len(awy) - 1):
            wpt2 = databaseManager.loadWpt(awy[i + 1][0])
            leg = Leg.TFLeg(wpt1, wpt2, seq, awy[i + 1][3], awy[i + 1][4], routeSeq)
            self.listLegs.insert(seq, leg)
            seq += 1
            wpt1 = wpt2
        databaseManager.close_connection()
        return seq

    def afficher(self):
        if self.listLegs == []:
            print("Le plan de vol n'a pas été initialisé")
        else:
            for i in range(len(self.listLegs)):
                leg = self.listLegs[i]
                display = leg.message()
                if leg == self.activeLeg:
                    display = "-> " + display
                print(display)
        pass

    def LongTermList(self):
        message = ""
        for i in range(len(self.listLegs) - 1):
            leg = self.listLegs[i]
            message = message + leg.message() + "; "

        leg = self.listLegs[len(self.listLegs) - 1]
        message = message + leg.message()
        return message

    def insertSegment(self, seqStartChange, changeRouteSeq, newSegment):
        seq = seqStartChange
        routeSeq = changeRouteSeq
        self.listLegs[seq - 1].afficher()
        for couple in newSegment:
            if couple[0] == 'DIRECT':
                seq = self.addDirect(couple[1], routeSeq, seq)
            else:
                seq = self.addAirway(couple[0], couple[1], routeSeq, seq)
            routeSeq += 1
        # Reséquencement des legs
        for i in range(seq, len(self.listLegs)):
            leg = self.listLegs[i]
            leg.seq = i
            leg.routeSeq += len(newSegment)

    def change(self, changeRouteSeqStart, changeRouteSeqEnd, newSegment):
        # Suppression des legs concernées par le changement
        changeLegSeqStart = 0
        changeLegSeqEnd = 0
        for i in range(1, len(self.listLegs)):
            if (self.listLegs[i].routeSeq == changeRouteSeqStart) and (
                    self.listLegs[i - 1].routeSeq != changeRouteSeqStart):
                changeLegSeqStart = i
            elif (self.listLegs[i].routeSeq != changeRouteSeqEnd) and (
                    self.listLegs[i - 1].routeSeq == changeRouteSeqEnd):
                changeLegSeqEnd = i
        newList = self.listLegs[:changeLegSeqStart] + self.listLegs[changeLegSeqEnd:]
        self.listLegs = newList

        # insertion des nouvelles legs
        seq = changeLegSeqStart
        routeSeq = changeRouteSeqStart
        for couple in newSegment:
            if couple[0] == 'DIRECT':
                seq = self.addDirect(couple[1], routeSeq, seq)
            else:
                seq = self.addAirway(couple[0], couple[1], routeSeq, seq)
            routeSeq += 1

        # Reséquencement des legs
        for i in range(seq, len(self.listLegs)):
            leg = self.listLegs[i]
            leg.seq = i
            leg.routeSeq += len(newSegment) - (changeRouteSeqEnd - changeRouteSeqStart + 1)

    def changeSegment(self, seqStartChange, changeRouteSeq, newSegment):
        seq = seqStartChange
        routeSeq = changeRouteSeq
        for couple in newSegment:
            if couple[0] == 'DIRECT':
                seq = self.addDirect(couple[1], routeSeq, seq)
            else:
                seq = self.addAirway(couple[0], couple[1], routeSeq, seq)
            routeSeq += 1
        # Reséquencement des legs
        for i in range(seq, len(self.listLegs)):
            leg = self.listLegs[i]
            leg.seq = i
            leg.routeSeq += len(newSegment) - 1
