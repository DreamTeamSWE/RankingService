class Database:
    def __init__(self):
        self.__clusterArn = None
        self.__secretArn  = None

    def doWriteQuery(self, query: str):
        pass

    def doReadQuery(self, query: str):
        pass

    def __parseResult(self, result):
        pass