import Route
import FlightPlan
import threading
import IhmManager
import DatabaseManager
import CommunicationManager


def ihm(FPLN_Route, FPLN_Leg, FPLN_temporary, communicationManager):
    ihmManager = IhmManager.IhmManager(FPLN_Route, FPLN_Leg, FPLN_temporary, communicationManager)
    ihmManager.run()
    pass

if __name__=="__main__":

    FPLN_Route = Route.Route()
    FPLN_Leg = FlightPlan.FlightPlan()
    FPLN_temporary = FlightPlan.FlightPlan()

    communicationManager = CommunicationManager.CommunicationManager(FPLN_Route, FPLN_Leg, FPLN_temporary)

    ihmThread = threading.Thread(target=ihm, args=(FPLN_Route, FPLN_Leg, FPLN_temporary, communicationManager))
    ihmThread.start()


    communicationManager.run()


