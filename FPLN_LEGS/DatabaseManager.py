import sqlite3
import Waypoint
import DatabaseException

class Database_Manager:
    def __init__(self):
        self.conn = sqlite3.connect("../navDB/data/nav.db")
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    #Recherche et téléchargement des données d'un aéroport
    def loadAirport(self, idAirport):
        self.cursor.execute("""SELECT latitude, longitude 
                                    FROM aeroport
                                    WHERE identifiant = '{}'""".format(idAirport))
        rows = self.cursor.fetchall()
        if rows == []:
            raise DatabaseException.DatabaseNotFoundException("Airport", idAirport)
        else:
            latitude = rows[0][0]
            longitude = rows[0][1]
            return latitude, longitude

    #Recherche et téléchargement des données d'un waypoint
    def loadWpt(self, idWpt):
        self.cursor.execute("""SELECT identifiant, latitude, longitude 
                            FROM waypoint
                            WHERE identifiant = '{}'""".format(idWpt))
        rows = self.cursor.fetchall()
        if rows == []:
            raise DatabaseException.DatabaseNotFoundException("waypoint", idWpt)
        else:
            latitude = rows[0][1]
            longitude = rows[0][2]
            waypoint = Waypoint.Waypoint(idWpt, latitude, longitude)
        return waypoint

    # Recherche et téléchargement des données d'un waypoint d'entrée d'un airway
    def loadEntryWpt(self, routeidentifier, Wpt):
        #Verification de l'existence de la route:
        self.cursor.execute("""SELECT * 
                                            FROM route
                                            WHERE routeidentifiant = '{}'""".format(routeidentifier))
        rows = self.cursor.fetchall()
        if rows == []:
            raise DatabaseException.DatabaseNotFoundException("Airways ", routeidentifier)
        else:
            #Si la route existe, on continue la recherche du waypoint d'entrée.
            self.cursor.execute("""SELECT sequencenumber, fixidentifiant 
                                        FROM route
                                        WHERE routeidentifiant = '{}' and fixidentifiant = '{}'""".format(routeidentifier, Wpt.id))
            rows = self.cursor.fetchall()
            if rows != []:
                return rows[0][0], Wpt
            else:
                self.cursor.execute("""select sequencenumber, fixidentifiant 
                                            from route where routeidentifiant = '{}' 
                                            and sequencenumber = (select MIN(sequencenumber) from route where routeidentifiant = '{}')""".format(routeidentifier, routeidentifier))
                rows = self.cursor.fetchall()
                if rows == []:
                    raise DatabaseException.DatabaseNotFoundException("EntryWaypoint of airways "+routeidentifier, Wpt.id)
                else:
                    wptEntry = self.loadWpt(rows[0][1])
                    return rows[0][0], wptEntry
        pass

    # Recherche et téléchargement des données d'un waypoint de sortie d'une airways
    def loadExitWpt(self, routeidentifier, idWpt):
        # Verification de l'existence de la route:
        self.cursor.execute("""SELECT * 
                                                    FROM route
                                                    WHERE routeidentifiant = '{}'""".format(routeidentifier))
        rows = self.cursor.fetchall()
        if rows == []:
            raise DatabaseException.DatabaseNotFoundException("Airway", routeidentifier)
        else:
        # Si la route existe, on continue la recherche du waypoint d'entrée.
            self.cursor.execute("""SELECT sequencenumber, fixidentifiant 
                                        FROM route
                                        WHERE routeidentifiant = '{}' and fixidentifiant = '{}'""".format(routeidentifier, idWpt))
            rows = self.cursor.fetchall()
            if rows == []:
                raise DatabaseException.DatabaseNotFoundException("Exit Waypoint of airways " + routeidentifier, idWpt)
            else:
                return rows[0][0], rows[0][1]

    #Recherche et téléchargement des données d'une airway (toutes les legs présentes entre les wpt d'entrée et de sortie)
    def loadAwy(self, routeidentifier, seqNumEntryWpt, seqNumExitWpt):
        if int(seqNumEntryWpt) <= int(seqNumExitWpt):
            self.cursor.execute("""SELECT fixidentifiant, outboundmagneticcruise, routefromdistance, minaltitude, maxaltitude
                                        FROM route 
                                        WHERE routeidentifiant = '{}' 
                                        AND sequencenumber >= '{}' 
                                        AND sequencenumber <= '{}'""".format(routeidentifier, seqNumEntryWpt, seqNumExitWpt))
            rows = self.cursor.fetchall()
            if rows == []:
                raise DatabaseException.DatabaseNotFoundException("Airways", routeidentifier)
            else:
                return rows
        else:
            self.cursor.execute("""SELECT fixidentifiant, outboundmagneticcruise, routefromdistance, minaltitude, maxaltitude
                                                    FROM route 
                                                    WHERE routeidentifiant = '{}' 
                                                    AND sequencenumber >= '{}' 
                                                    AND sequencenumber <= '{}'""".format(routeidentifier, seqNumExitWpt, seqNumEntryWpt))
            rows = self.cursor.fetchall()
            if rows == []:
                raise DatabaseException.DatabaseNotFoundException("Airways", routeidentifier)
            else:
                rows.reverse()
                return rows

