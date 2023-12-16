class Route:
    def __init__(self):
        self.departure = None
        self.arrival = None
        self.listRoute = []

    def initRoute(self, DEP, ARR, FPLN_Route):
        self.departure = DEP
        self.arrival = ARR
        reformat = FPLN_Route.split(", ")
        for i in range(len(reformat)):
            routeidentifiant = reformat[i].split("-")[0]
            fixidentifiant = reformat[i].split("-")[1]
            reformat[i] = (routeidentifiant, fixidentifiant)

        self.listRoute = reformat

    def change(self, changeRouteSeqStart, changeRouteSeqEnd, newSegment):
        self.listRoute[changeRouteSeqStart:changeRouteSeqEnd+1] = newSegment
        pass

    def afficher(self):
        print(self.listRoute)
        pass
