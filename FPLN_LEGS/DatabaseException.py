class DatabaseNotFoundException(Exception):

    def __init__(self, typeData, data):
        Exception.__init__(self, typeData, data)
        self.data = data
        self.typeData = typeData

    def __str__(self):
        return "exception DatabaseNotFound: la donnée {0} de type {1} n'a pas été trouvée dans la database".format(self.data, self.typeData)
