# Main application class
# @author florian.blaud

"""
Classes and functions table
"""

import logging
from typing import Optional
from ivy.std_api import *
from scanner import Scanner

class MainFplnRoute:
    communication_manager = None
    active_fpln = None
    scanner = None

    def __init__(self, domain: Optional[str] = "127.255.255.255:2010"):
        self.domain = domain

    def main(self, args):
        logging.error("") # equivalent of System.err.close()
        index = 0
        while index < len(args):
            opt = args[index]
            if opt == "-b":
                self.domain = args[index + 1]
                print(self.domain)
            elif not opt.isEmpty() and opt[0] == "-":
                logging.error(f"Unknown option: '{opt}'")
            index += 1

        try:
            self.communication_manager = CommunicationManager(self.domain)
        except IvyException as ex:
            logging.error(f"Impossible to connect to the domain {self.domain}")
            logging.error(ex)
        self.active_fpln = Fpln()
        self.scanner = Scanner(sys.stdin)
        Menu.manage(self.active_fpln, self.communication_manager, self.scanner)

if __name__ == "__main__":
    MainFplnRoute().main(sys.argv[1:])
