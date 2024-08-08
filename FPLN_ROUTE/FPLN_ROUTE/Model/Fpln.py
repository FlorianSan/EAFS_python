"""Modified by Adama YAYA : 02/02/2024
"""

from FPLN_ROUTE.Model.Airport import Airport
from FPLN_ROUTE.Model.Ndb import Ndb
import pandas as pd

class Fpln:
    """
    Flight plan class
    """
    def __init__(self):
        """
        Departure and arrival airport objects
        """
        self.airportDep = Airport()
        self.airportArr = Airport()
        """
        Route : List of sections (airway identifier and waypoint identifier couple)
        airways and waypoints are not java object, only defined by a string (identifier)
        """
        # self.route = []
        self.route = None
        """ 
        Number of segments in the route
        """
        self.routeSize = 0

        """
        File path
        """
        self.ndbPath = 'C:/Users/yayaa/PycharmProjects/EAFS/navDB/data/csv'

        # List of airport in the navDB
        self.aptList = []
        self.apt_list('/aeroport.csv')

    def addSection(self, awyId, wptId):
        """
        Add couple to list of airway identifier and waypoint identifier couples
        
        @param awyId airway identifier
        @param wptId waypoint identifier
        @return list of boolean checkList: 
          -1st element : Airway existence
          -2nd element : Previous Waypoint existence in current Airway
          -3rd element : Waypoint existence 
          -4th element : Waypoint existence in Airway
        """
        """
        checkList initialisation
        """
        checkList = [False] * 4
        awyExist = False
        prevWptInAwy = False
        wptExist = False
        wptInAwy = False
        
        """
        Empty segment creation
        """
        segment = []
        
        """ 
        Verifications in NDB:
        Airway-Waypoint existence verification
        Current and previous Waypoint affiliations in Airway verification
        
        Update of checkList status
        """
        if awyId == "DIRECT":
            #Special case when user enters the first/last route segment
            awyExist = True
            checkList[0] = awyExist
            prevWptInAwy = True
            checkList[1] = prevWptInAwy
            if wptId == "STAR":
                # User has entered the last route segment
                wptExist = True
                checkList[2] = wptExist
                wptInAwy = True
                # checkList[3] = wptIn  :: code line found
                checkList[3] = wptInAwy  # modification
                # couple filling
                segment.append(awyId)
                segment.append(wptId)
                
                # Adding the couple to the sequenceList
                self.route.append(segment)
                self.routeSize += 1
            else:
                #User has entered the first route segment
                wptExist = Ndb.checkExist(wptId, "waypoint", "identifiant")
                checkList[2] = wptExist
                if wptExist:
                    wptInAwy = True
                    checkList[3] = wptInAwy
                    
                    # couple filling
                    segment.append(awyId)
                    segment.append(wptId)
                    
                    # Adding the couple to the sequenceList
                    self.route.append(segment)
                    self.routeSize += 1
        else:
            #User has entered a classical route segment
            
            #Waypoint recovery of the previous route segment
            prevSegment = self.route[self.routeSize - 1]
            prevWptId = prevSegment[1]
            #Airway existence verification
            awyExist = Ndb.checkExist(awyId, "route", "routeidentifiant")
            checkList[0] = awyExist
            wptExist = Ndb.checkExist(wptId, "route", "fixidentifiant")
            checkList[2] = wptExist
            if awyExist:
                # Verification of previous Waypoint affiliations in Airway
                prevWptInAwy = Ndb.checkWptInAwy(awyId, prevWptId)
                checkList[1] = prevWptInAwy
            if awyExist and wptExist:
                # Verification of Waypoint affiliations in Airway
                wptInAwy = Ndb.checkWptInAwy(awyId, prevWptId)
                checkList[3] = wptInAwy
            if awyExist and prevWptInAwy and wptExist and wptInAwy:  
                # couple filling
                segment.append(awyId)
                segment.append(wptId)
                
                # Adding the couple to the sequenceList
                self.route.append(segment)
                self.routeSize += 1
        return checkList
    
    def getAirportDep(self):
        """
        Get departure Airport  
        @return departure Airport
        """
        return self.airportDep
    
    def getAirportArr(self):
        """
        Get arrival Airport  
        @return departure Airport
        """
        return self.airportArr
    
    def getRoute(self):
        """
        Get route  
        @return route
        """
        return self.route
    
    def getRouteSize(self):
        """
        Get number of segments in the route  
        @return routeSize
        """
        return self.routeSize
    
    def setAirportDep(self, identifier):
        """
        Set departure airport identifier
        
        @param identifier Airport identifier
        @return boolean
        """
        # Airport existence verification in NDB
        # exist = Ndb().checkExist(data=identifier,table="aeroport",column="identifiant")
        # la ligne du dessus est pas complette 
		# boolean exist = Ndb.checkExist(identifier, "aeroport", "identifiant")
        exist = True

        if identifier in self.aptList:
            self.airportDep.setIdentifier(identifier)
        else:
            print('the departure airport selected is not in the database')
            exist = False
        return exist
    
    def setAirportArr(self, identifier):
        """
        Set arrival airport identifier
        
        @param identifier Airport identifier
        @return boolean
        """
        # Airport existence verification in NDB
        # exist = Ndb.checkExist(self,data=identifier, table="aeroport", column="identifiant")
        exist = True
        if identifier in self.aptList:
            self.airportArr.setIdentifier(identifier)
        else:
            print('the arrival airport selected is not in the database')
            exist = False
        return exist
    
    def setRoute(self, newRoute):
        """
        Set route
        @param newRoute
        """
        self.routeSize = len(newRoute)
        # self.route.clear()
        self.route = newRoute
        # self.route.extend(newRoute)
    
    def copyFpln(self, fpln):
        """
        Copy a flight plan in another - generally active flight plan in temporary flight plan
        @param fpln 
        """
        self.setAirportDep(fpln.getAirportDep().getIdentifier())
        self.setAirportArr(fpln.getAirportArr().getIdentifier())        
        self.setAirportArr(fpln.getAirportArr().getIdentifier())
        self.setRoute(fpln.getRoute())
    
    def insertSectionInRoute(self, i, section):
        """
        Insert a section in the route just after the section number i
        @param i
        @param section
        """
        self.route.insert(i, section)
        self.routeSize += 1
    
    def changeSectionInRoute(self, i, section):
        """
        Change the section number i in the route
        @param i
        @param section
        """
        self.route[i] = section
    
    def removeRouteSection(self, i):
        """
        Update the route by deleting section number i
        @param i
        """
        self.route.remove(i)
        self.routeSize -= 1
    
    def removeRouteSection(self, iStart, iEnd):
        """
        Update the route by deleting sections between indexStart (included) and indexEnd(included)
        @param iStart
        @param iEnd
        """
        for i in range(0, (iEnd-iStart)):
            self.route.remove(iStart)
        self.routeSize -= (iEnd - iStart + 1)
    
    def clearRoute(self):
        """
        Erase all the route.
        """
        self.route.clear()
        self.routeSize = 0
 
    def apt_list(self,file):
        _file = self.ndbPath + file
        df = pd.read_csv(_file)
        for i in range(len(df)):
            self.aptList.append(str(df.iloc[i,0]).split(';')[2])

