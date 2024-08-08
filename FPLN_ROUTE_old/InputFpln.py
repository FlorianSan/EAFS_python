

class InputFpln:
    def inputFpln(self, fpln, scanner):
        print("\nFPLN TAB")
        print("-------------------------")
        self.inputAirportDep(fpln, scanner)
        self.inputAirportArr(fpln, scanner)
        self.inputRoute(fpln, scanner)
        print("Fpln successfully filled !")

    def inputAirportDep(self, fpln, scanner):
        exist = False
        fromAptId = ""

        while exist == False:
            print("\nType departure APT and press Enter : ")
            fromAptId = scanner.next()
            exist = fpln.setAirportDep(fromAptId.upper())
            if exist == False:
                print("==> INVALID ENTRY")

        fromAptIdInput = fpln.getAirportDep().getIdentifier()
        print("==> FromAPT "+fromAptIdInput+" successfully added to FPLN !")

    def inputAirportArr(self, fpln, scanner):
        exist = False
        toAptId = ""

        while exist == False:
            print("\nType arrival APT and press Enter : ")
            toAptId = scanner.next()
            exist = fpln.setAirportArr(toAptId.upper())
            if exist == False:
                print("==> INVALID ENTRY")

        toAptIdInput = fpln.getAirportArr().getIdentifier()
        print("==> ToAPT "+toAptIdInput+" successfully added to FPLN !")




def inputRoute(fpln, scanner):
    checkList= []
    awyExist = False
    prevWptInAwy = False
    wptExist = False
    wptInAwy = False
    choice = ""
    awyId = ""
    wptId = ""
    awyIdInput = ""
    wptIdInput = ""
    cpt = 0 #counter to find out if this is the first time we pass through the input verification loop
    routeSize = 0

    fpln.clearRoute()
    while choice.upper() != "ACTIVATE":
        #System.out.println(fpln.getRoute())
        print("\nType AWY WPT to enter a section\nType DEL to delete the previous entry\nType ACTIVATE when you are done")
        awyId = scanner.next().upper()
        if awyId == "ACTIVATE": #Pilot types "ACTIVATE" to end route entry and to activate it
            if awyIdInput == "DIRECT" and wptIdInput == "STAR":
                choice = awyId
            else:
                print("==> IMPOSSIBLE ACTIVAION: You must finish by DIRECT-STAR section !")
        elif awyId == "DEL": #Pilot types "DEL" to delete his previous entry
            if fpln.getRouteSize() == 0:
                print("==> The route does not yet have a section !")
            else:
                fpln.removeRouteSection(routeSize-1)
                print("==> Section "+awyIdInput+"-"+wptIdInput+" deleted !")
        else:
            while awyExist == False or prevWptInAwy == False or wptExist == False or wptInAwy == False:
                #System.out.println("Type AWY WPT E to Enter a segment\nType AWY WPT ACTIVATE if last segment")
                if cpt != 0:
                    print("\nType AWY WPT to enter a section\nType DEL to delete the previous entry\nType ACTIVATE when you are done")
                    awyId = scanner.next().upper()
                if awyId == "ACTIVATE": #Pilot types "ACTIVATE" to end route entry and to activate it
                    if awyIdInput == "DIRECT" and wptIdInput == "STAR":
                        choice = awyId
                        #Booleans reset to be able to check the next section entry
                        awyExist = True
                        prevWptInAwy = True
                        wptExist = True
                        wptInAwy = True
                    else:
                        print("==> IMPOSSIBLE ACTIVATION: The route must finish by a section DIRECT-STAR !")
                elif awyId == "DEL": #Pilot types "DEL" to delete his previous entry
                    if fpln.get_route_size() == 0:
                        print("==> The route does not yet have a section !")
                else:
                    fpln.remove_route_section(route_size-1)
                    print("==> Section "+awy_id_input+"-"+wpt_id_input+" deleted !")
                    # Booleans reset to be able to check the next section entry
                    awy_exist = True
                    prev_wpt_in_awy = True
                    wpt_exist = True
                    wpt_in_awy = True
                    
                # Booleans reset to be able to check the next section entry
                awy_exist = False
                prev_wpt_in_awy = False
                wpt_exist = False
                wpt_in_awy = False
                cpt = 0

                if not awyId == "DEL" and not awyId == "ACTIVATE":
                    route_size = fpln.get_route_size()
                    awy_id_input = fpln.get_route()[route_size-1][0] #get the airway idenifier of the input section 
                    wpt_id_input = fpln.get_route()[route_size-1][1] #get the waypoint idenifier of the input section 
                    print("==> Section " +awy_id_input+"-"+wpt_id_input+" successfully added to route !")

                print("\nRoute successfully added to FPLN !")

                pass