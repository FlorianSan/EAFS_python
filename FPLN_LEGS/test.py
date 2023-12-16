

import Route
import FlightPlan
import DatabaseManager
import Waypoint


if __name__=="__main__":
    # db =DatabaseManager.Database_Manager()
    # test = db.loadEntryWpt("UM733", "OKTET")
    # print(test)

    route = "DIRECT-OKTET, UM733-BULOL, UZ12-ATN, UM976-OKRIX, UH10-AGOGO, DIRECT-STAR"
    route = Route.Route("LFMN", "LFRG", route)
    print(route.listRoute)
    test = FlightPlan.FlightPlan(route)
    test.afficher()




#"FROM=LFMN TO=LFRG ROUTE=DIRECT-OKTET, UM733-BULOL, UZ12-ATN, UM976-OKRIX, UH10-AGOGO, DIRECT-STAR"