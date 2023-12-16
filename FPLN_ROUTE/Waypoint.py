"""
Class to manage and to get Waypoint Information

author Pierre-Antoine
"""
class Waypoint:
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
        Set Waypoint identifier
        """
        self.identifier = identifier

    def getIdentifier(self):
        """
        Get Waypoint identifier
        """
        return self.identifier