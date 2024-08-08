from ivy.std_api import IvyStart, IvyStop, IvyInit, IvyBindMsg, IvySendMsg
import time
import threading

# @author florian.blaud



#Global variables to store pieces of information
bus = "" # bus to allow communication with other teams
currentTime = 0 #helps building the timestamp of the messages we send
currentFplnString = "" # Current route with string message format
lastModifMsg = ""  # Last modification
flying = False  # allow to know if we are inflight or no
activeSection = 0  # airway active
aptSim = ""  # simulation airport identifier
AP_Mode = ""
modifMsgReceived = False



# React to messages : in this section, you can find the r_functions
# (the reaction functions triggered after reception of a specific message)

def r_updateTime(*arg):
    global currentTime
    currentTime=arg[0]
    
def r_sendInitFplnAgain(*arg):
    print("FL_Error Receiving Flight Plan")
    sendInitFplnAgain()
    updateDisplay()
    
def r_sendModifAgain(*arg):
    print("FL_Error Receiving Modified Route")
    sendModifAgain()
    updateDisplay()
    
def r_AA(*arg):
    global activeSection
    temp=int(arg[1])
    if activeSection<temp:
        activeSection=temp
        updateDisplay()
        
def r_APStateMode(*arg):
    global AP_Mode
    if AP_Mode != arg[2]:
        AP_Mode = arg[2]
        print("\n\nSwitch to"+arg[2]+" mode\n")
        updateDisplay()

def r_FlightStartedOrNot(*arg):
    global flying
    if flying== False: #Original simplification
        flying= True
        print("\n\nThe flight start")
        updateDisplay()
        
def r_SimAptId(*arg):
    global aptSim
    aptSim=arg[0]
    print("Simulation airport is "+aptSim)
    
def r_ModifReady(*arg):
    t1=threading.Thread(target=chrono, args=(7,))
    t1.start()
def chrono(s):
    time.sleep(s)
    
def r_ModifMessage(*arg):
    global modifMsgReceived
    modifMsgReceived= True
    numStart=int(arg[1])
    numEnd=int(arg[2])
    updateRoute(numStart, numEnd, arg[3])
    print("\nRoute modification received from LEGS")
    updateDisplay()
    
def r_StopBus():
    bus.stop()
    

    
# Send messages

##FLIGHT PLAN INITIALIZATION

#Send a message regarding the ROUTE via Ivy bus
# @param header, object of the message
# @param message
def sendFR(header,message):
    try :
        whole_message = "FL_" + header + "Time=" + currentTime + " " + message
        IvySendMsg(whole_message)
        print(whole_message)
    except Exception:
        print("Sending error.")
       
# Send a message on the bus once the flight plan is ready i.e READY button is clicked on the HMI
def sendReady():
    sendFR("Ready", "Initial Flight Plan Ready")
    
# Send the flight plan on the bus once INIT button is clicked on the HMI
# Message "FR_InitFlightPlan Time=currentTime FROM=identifiant TO=identifiant ROUTE=routeidentifiant-fixidentifiant, routeidentifiant-fixidentifiant, routeidentifiant-fixidentifiant
# FROM = departure airport (identifiant in the Airport table of the NavDB)
# TO = arrival airport (identifiant in the Airport table of the NavDB)
# ROUTE (P1) = airway-waypoint (routeidentifiant of an airway in Route table of the NavDB, fixidentifiant of a waypoint in Route table of the NavDB (== to identifiant of Waypoint table))
# @param fpln flight plan object
def sendInitFpln(fpln):
    fplnString = createMsg(fpln)
    global currentFplnString
    currentFplnString=fplnString
    sendFR("InitFlightPlan", fplnString)
    
# Send the flight plan again by using the currentFplnString
def sendInitFplnAgain():
    sendReady()
    sendFR("InitFlightPlan",currentFplnString)
    
#Send a error message when simulation airport is unknown. 
def sendErrorAptSim():
    sendFR("ERROR","Error Receiving Simulation Airport Identifier")
    
##FLIGHT PLAN MODIFICATION

# Send message to informe LEGS that we do not received their modification.
def sendErrorModifReception():
    sendFR("ERROR","Error Receiving Modified Route")

# Send a message on the bus once the modif is ready i.e READY button is clicked on the HMI.
# Message "FR_ModifReady Time=currentTime Modified Flight Plan Ready"
def sendModifReady():
    sendFR("ModifReady", "Modified Flight Plan Ready")

# Send the modif on the bus once INIT button is clicked on the HMI
# @param modif 
#   if change: ["CHG", "num of replaced segment", "new portion with format AWY-WPT"]
#       Message "FR_CHG Time=currentTime numModifiedSegment=num newRoutePortion=AWY1-WPT1, AWY2-WPT2..."
#   insertion: ["INS", "num of replaced segment", "new portion with format AWY-WPT"]
#       Message "FR_INS Time=currentTime numModifiedSegment=num newRoutePortion=AWY1-WPT1, AWY2-WPT2..."
def sendingModifFpln(modif):
    global lastModifMsg
    lastModifMsg=createMsg(modif)
    sendFR("Modif", lastModifMsg)
    ModifFpln.setModifReady(False)
    
# Send the modif again by using the lastModifMsg
def sendModifAgain():
    sendModifReady()
    sendFR("Modif", lastModifMsg)
    
    
    
# Message Formating

# Create the string message which will contain the flight plan
# @param fpln flight plan object
# @return String message
def createMsg(fpln):
    airportDep = fpln.getAirportDep()
    airportArr = fpln.getAirportArr()
    route = fpln.getRoute()
    routeSize = fpln.getRouteSize()
    
    #Addition of departure and arrival airports
    fplnString = "FROM=" + airportDep.getIdentifier() + " TO=" + airportArr.getIdentifier() + " ROUTE="
    
    #Adition of the route
    for i in range(0,routeSize-1):
        fplnString += (route.get(i)).get(0) + "-" + (route.get(i)).get(1) + ", "
    fplnString += (route.get(routeSize - 1)).get(0) + "-" + (route.get(routeSize - 1)).get(1);
    return fplnString
        

# Create the string message which will contain the new route portion of the modified flight plan
# @param modif
# @return String message "numModifiedSegment=num newRoutePortion=AWY1-WPT1, AWY2-WPT2..."
def createMsg(modif):
        modifString = "numStart="+modif.get(0)+" numEnd="+modif.get(1)+" ModifiedSection="+modif.get(2)
        return modifString
    
    
    
# Display update (after active airway reception)
    #Method to update information display
def updateDisplay():
    choice=Menu.getMenuChoice()
    if choice=="":
            Menu.printMenu()
            print("Enter the number of this section: ")
    elif choice=="5":
            updateRouteDisplay()
                
# Method to update route display
def updateRouteDisplay():
        routeToDisplay = MainFplnRoute.activeFpln.getRoute()
        routeSize = MainFplnRoute.activeFpln.getRouteSize()

        print("\n\nROUTE TAB")
        print("-------------------------")
        if (flying==False):
            for i in range(0,routeSize):
                print(routeToDisplay.get(i).get(0)+" - "+routeToDisplay.get(i).get(1))
        else :
            if (activeSection != 0):
                print("  (SEQ)  -- " + routeToDisplay.get(activeSection - 1).get(0) + " - " + routeToDisplay.get(activeSection - 1).get(1))
                print("  (ACT)  -- " + routeToDisplay.get(activeSection).get(0) + " - " + routeToDisplay.get(activeSection).get(1))
            elif (activeSection == (routeSize - 2)) :
                print(" (NoSEQ) -- " + routeToDisplay.get(activeSection + 1).get(0) + " - " + routeToDisplay.get(activeSection + 1).get(1))
            elif (activeSection <= (routeSize - 3)) :
                print(" (NoSEQ) -- " + routeToDisplay.get(activeSection + 1).get(0) + " - " + routeToDisplay.get(activeSection + 1).get(1))
                print(" (NoSEQ) -- " + routeToDisplay.get(activeSection + 2).get(0) + " - " + routeToDisplay.get(activeSection + 2).get(1))
        print("-------------------------")
        print("Enter 0 to quit ROUTE TAB: ")

                
                
# Aircraft state related methods 

# Set the state of modification message reception
def setModifMsgReceived(state):
    global modifMsgReceived
    modifMsgReceived = state
    
    
    
# Update Route (after modif reception from LEG)
    
#  Method to update the flight plan after the reception of modification by LEGS
def updateRoute(indexStart, indexEnd, modifRoute):
    modifiedRouteList = modifRoute.split(", ")
    sizeModif = modifiedRouteList.length
    MainFplnRoute.activeFpln.removeRouteSection(indexStart, indexEnd)
    nbTemp = indexStart

    for i in range(0,sizeModif):
        sTemp = modifiedRouteList[i].split("-")
        sect = []
        sect.add(sTemp[0])
        sect.add(sTemp[1])
        MainFplnRoute.activeFpln.insertSectionInRoute(nbTemp, sect)
        nbTemp=nbTemp + 1
    

# initialize (set up the bus, name and ready message)
bus = IvyInit("FPLN_ROUTE_APP", "FPLN_ROUTE Ready", 0)

#Here you can find all the messages binding

# update current time value for message timestamping
IvyBindMsg(r_updateTime,"^Time t=(.*)")

# Send flight plan another time if not received by LEGS
IvyBindMsg(r_sendInitFplnAgain,"^FL_ERROR Time=(.*) Error Receiving Flight Plan")

# Send modified route another time if not received by LEGS
IvyBindMsg(r_sendModifAgain,"^FL_ERROR Time=(.*) Error Receiving Modified Route")

# Listen to FPLN-LEGS to get the sequence number of the active airway
# to show on which segment on the route is the A/C
IvyBindMsg(r_AA,"FL_AA Time=(.*) NumActiveAwy=(.*)")

# Listen to GUID-COMM to get the auto pilot state 
# Display needs to match selected/managed mode
IvyBindMsg(r_APStateMode, "GC_AP Time=(.*) AP_State='(.*)' AP_Mode='(.*)'")

# Listen to GUID-TRAJ to known when the flight start 
# Allow to manage authorized modification
IvyBindMsg(r_FlightStartedOrNot,"^InitStateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)")

# Listen to SIM-PARAM to get the simulation airport
# SIM_PARM is the module which deals with simulation parameters and launches the start of the simulation 
IvyBindMsg(r_SimAptId,"^SP_AptId Identifier=(.*)")

# Listen to FPLN-LEGS ready message for modification
IvyBindMsg(r_ModifReady,"FL_ModifReady Time=(.*) Modified Flight Plan Ready")

# Listen to FPLN-LEGS to get the route modification
# FL_Modif Time=0  numStart=1 numEnd=2 ModifiedSection=UY156-PERIG, DIRECT-NORON, DIRECT-DIBAG
IvyBindMsg(r_ModifMessage,"FL_Modif Time=(.*) numStart=(.*) numEnd=(.*) ModifiedSection=(.*)")

# start the bus on specified domain 
IvyStart(bus)

# Stop the bus when main application asks
IvyBindMsg(r_StopBus,"^Stop")








        
