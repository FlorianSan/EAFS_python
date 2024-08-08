""" Author: Pierre-Antoine Chabbert """



class Airway:
    """
    Class to manage and to get Waypoint Information
    """

    def __init__(self):
        """
        Constructor
        """
        self.identifier = ""

    def setIdentifier(self, identifier):
        """
        Set Airway identifier
        """
        self.identifier = identifier

    def getIdentifier(self):
        """
        Get Airway identifier
        """
        return self.identifier
