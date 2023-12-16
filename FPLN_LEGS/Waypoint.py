class Waypoint:
    def __init__(self, ident, lat, long):
        self.id = ident
        self.type = "Flyby"
        self.latitude = lat
        self.longitude = long
        self.norm_latitude = self.normalize_latitude(self.latitude)
        self.norm_longitude = self.normalize_longitude(self.longitude)

    def normalize_latitude(self, latitude):
        NS, norm_latitude = latitude[0], latitude[1:]
        if NS == 'N':
            norm_latitude = int(norm_latitude) * 10 ** (-6)
        else:
            norm_latitude = - int(norm_latitude) * 10 ** (-6)
        return norm_latitude

    def normalize_longitude(self, longitude):
        EO, norm_longitude = longitude[0], longitude[1:]
        if EO == 'E':
            norm_longitude = int(norm_longitude) * 10 ** (-6)
        else:
            norm_longitude = -int(norm_longitude) * 10 ** (-6)
        return norm_longitude