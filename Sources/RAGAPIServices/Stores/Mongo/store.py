from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from bson import ObjectId
from Utils.ConfigParserUtil import ConfigParserUtil
from Utils.LoggerUtil import LoggerUtil
from Handlers.RagapiServicesException import RagapiservicesException
from Handlers.ErrorCodes import ERR_MONGO_DB_CONN_FAILED

class MongoDBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    def __init__(self):
        self.config = ConfigParserUtil()
        host = self.config.getValue("MongoDB", "Host")
        port = self.config.getValue("MongoDB", "Port")
        username = self.config.getValue("MongoDB", "Username")
        password = self.config.getValue("MongoDB", "Password")    
        serverTimeOut = self.config.getValue("MongoDB", "ServerTimeOut")
        mongoURI = "mongodb://" + username + ":" + password +  "@" + host + ":"  + port
        client = None
        try:
            client = MongoClient(mongoURI, serverSelectionTimeoutMS=serverTimeOut)
            db = client[self.config.getValue("MongoDB", "DatabaseName")]
            self._RegressionConfigcollection = db["RegressionConfig_TBD"]
            self._LiPiTicketscollection = db["LPiTickets"]
        except Exception as e:
            pass
            # self.logger.log_error("Exception: " + str(e))
            # raise RagapiservicesException(ERR_MONGO_DB_CONN_FAILED, host, port)

    def getRegressionConfigOne(self, branch):
        # self.logger.log_info("Getting regression config for branch: " + branch)
        result = self._RegressionConfigcollection.find_one({"Branch": branch})
        return result
    
    def getRegressionConfig(self, branch):
        # self.logger.log_info("Getting regression config for branch: " + branch)
        result = self._RegressionConfigcollection.find({"Branch": branch})
        return result
    
    def getLPiTicketOne(self):
        result = self._LiPiTicketscollection.find_one({"favoriteName": "enterprise_sim_memhooks"})
        return result
    
    def getLPiTickets(self):
        result = self._LiPiTicketscollection.find({"favoriteName": "enterprise_sim_memhooks"})
        return result

