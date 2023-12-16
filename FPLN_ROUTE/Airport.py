class Airport:
    """
    Airport identifier
    """
    def __init__(self):
        self.identifier = None
        """
        Airport identifier
        """

    def setIdentifier(self, identifier):
        """
        Set Airport identifier
        """
        self.identifier = identifier

    def getIdentifier(self):
        """
        Get Airport identifier
        """
        return self.identifier
