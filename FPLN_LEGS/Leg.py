import math

class IFLeg:
    def __init__(self, wpt):
        self.type = 'IF'
        self.seq = 0
        self.waypoint = wpt
        self.routeSeq = 0


    def message(self):
        message = "SEQ=" + str(self.seq) + " TYPE=" + self.type + " ID=" + self.waypoint.id + " LAT=" + self.waypoint.latitude + " LONG=" + self.waypoint.longitude
        return message

class TFLeg:
    def __init__(self, Wpt1, Wpt2, seq, minaltitude, maxaltitude, RouteSeq):
        self.type = 'TF'
        self.seq = seq
        self.routeSeq = RouteSeq
        self.waypointStart = Wpt1
        self.waypoint = Wpt2
        self.course = int(self.calcul_course())
        self.distance = int(self.calcul_distance())

        if minaltitude != "":
            self.minaltitude = minaltitude
        else:
            self.minaltitude = "FL000"

        if maxaltitude != "":
            self.maxaltitude = maxaltitude
        else:
            self.maxaltitude = "FL460"

    def setSeq(self, newSeq):
        self.seq = newSeq
        pass

    def calcul_course(self):
        latA, longA = math.radians(self.waypointStart.norm_latitude), math.radians(self.waypointStart.norm_longitude)
        latB, longB = math.radians(self.waypoint.norm_latitude), math.radians(self.waypoint.norm_longitude)
        X = math.cos(latB)*math.sin(longB-longA)
        Y = math.cos(latA)*math.sin(latB) - math.sin(latA)*math.cos(latB)*math.cos(longB-longA)
        course = math.atan2(X, Y)
        return math.degrees(course)%360

    def calcul_distance(self):
        latA, longA = math.radians(self.waypointStart.norm_latitude), math.radians(self.waypointStart.norm_longitude)
        latB, longB = math.radians(self.waypoint.norm_latitude), math.radians(self.waypoint.norm_longitude)
        distance = 60 * math.degrees(math.acos(math.cos(latA)*math.cos(latB)*math.cos(longB-longA) + math.sin(latA)*math.sin(latB)))
        return distance

    def message(self):
        message = "SEQ=" + str(self.seq) + " TYPE=" + self.type + " ID=" + self.waypoint.id + " WPT_TYPE=" + self.waypoint.type + " LAT=" + self.waypoint.latitude + " LONG=" + self.waypoint.longitude + " COURSE=" + str(self.course) + " DISTANCE=" + str(self.distance) + " FLmin=" + self.minaltitude + " FLmax=" + self.maxaltitude
        #message = "ID=" + self.waypoint.id + " SEQ=" + str(self.seq) + " LAT=" + self.waypoint.latitude + " LON=" + self.waypoint.longitude + " COURSE=" + str(self.course) + " FLY=" + self.waypoint.type + " FLmin=" + self.minaltitude + " FLmax=" + self.maxaltitude + " SPEEDmax=000"
        return message