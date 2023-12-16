import sqlite3


class Ndb:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = sqlite3.connect("../navDB/data/nav.db")
            self.cursor = self.connection.cursor()
        except Exception as error:
            print("Error while connecting to NDB", error)
    
    def disconnect(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            print("NDB connection is closed")
    
    def checkExist(self, data, table, column):
        try:
            self.cursor.execute("SELECT * from "+table+" where "+column+" = %s", (data,))
            row = self.cursor.fetchone()
            if row is not None:
                return True
            else:
                return False
        except Exception as error:
            print("Error while connecting to NDB", error)
    
    def checkWptInAwy(self, awyId, wptId):
        try:
            if awyId != "DIRECT":
                self.cursor.execute("SELECT * from route where routeidentifiant=%s and fixidentifiant=%s", (awyId, wptId))
                row = self.cursor.fetchone()
                if row is not None:
                    return True
                else:
                    return False
            else:
                return True
        except Exception as error:
            print("Error while connecting to NDB", error)
    
    def searchReachableAwy(self, wptId1, wptId2):
        try:
            self.cursor.execute("select routeidentifiant from route where routeidentifiant in (select routeidentifiant from route where fixidentifiant=%s) and fixidentifiant=%s", (wptId1, wptId2))
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                result.append(row[0])
            if len(result) == 0:
                result.append("DIRECT")
            return result
        except Exception as error:
            print("Error while connecting to NDB", error)
    
    def searchReachableWpt(self, wptDepId, wptArrId, awyId):
        try:
            self.cursor.execute("select sequencenumber from route where routeidentifiant=%s and fixidentifiant=%s", (awyId, wptDepId))
            row = self.cursor.fetchone()
            seqNbWptDep = row[0]
            self.cursor.execute("select sequencenumber from route where routeidentifiant=%s and fixidentifiant=%s", (awyId, wptArrId))
            row = self.cursor.fetchone()
            seqNbWptArr = row[0]
            if int(seqNbWptDep)<int(seqNbWptArr):
                self.cursor.execute("select sequencenumber, fixidentifiant from route where (routeidentifiant=%s) and (sequencenumber between %s and %s) and (sequencenumber!=%s) order by sequencenumber", (awyId, seqNbWptDep, seqNbWptArr, seqNbWptDep))
            else:
                self.cursor.execute("select sequencenumber, fixidentifiant from route where (routeidentifiant=%s) and (sequencenumber between %s and %s) and (sequencenumber!=%s) order by sequencenumber desc", (awyId, seqNbWptArr, seqNbWptDep, seqNbWptDep))
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                result.append(row[1])
            return result
        except Exception as error:
            print("Error while connecting to NDB", error)
    
    def searchPossibleWpt(self, refWptfId, currentWptId, awyId):
        try:
            self.cursor.execute("select sequencenumber from route where routeidentifiant=%s and fixidentifiant=%s", (awyId, refWptfId))
            row = self.cursor.fetchone()
            seqNbRefWpt = row[0]
            self.cursor.execute("select sequencenumber from route where routeidentifiant=%s and fixidentifiant=%s", (awyId, currentWptId))
            row = self.cursor.fetchone()
            seqNbCurrentWpt = row[0]
            if int(seqNbRefWpt)<int(seqNbCurrentWpt):
                self.cursor.execute("select sequencenumber, fixidentifiant from route where routeidentifiant=%s and sequencenumber>%s and sequencenumber!=%s order by sequencenumber", (awyId, seqNbRefWpt, seqNbCurrentWpt))
            else:
                self.cursor.execute("select sequencenumber, fixidentifiant from route where routeidentifiant=%s and sequencenumber<%s and sequencenumber!=%s order by sequencenumber desc", (awyId, seqNbRefWpt, seqNbCurrentWpt))
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                result.append(row[1])
            return result
        except Exception as error:
            print("Error while connecting to NDB", error)