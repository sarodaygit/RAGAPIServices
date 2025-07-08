ERR_CODE_GENERIC_ERROR = -1
ERR_CODE_NO_ERROR = 0
ERR_CODE_INVALID_WORKING_FOLDER_PATH_PROVIDED = 1
ERR_CODE_CANNOT_CREATE_WORKING_FOLDER_PATH = 2

ERR_CODE_REST_SERVER_WORKING_FOLDER_CREATE_FAILURE = 101
ERR_CODE_REST_SERVER_NOT_RUNNING = 102
ERR_CODE_REST_SERVER_ALREADY_RUNNING = 103
ERR_CODE_REST_SERVER_SHUTDOWN_REQUEST_FAILED = 104
ERR_CODE_REST_SERVER_SHUTDOWN_REQUEST_TIMEDOUT = 105
ERR_CODE_ERROR_WHILE_STARTING_REST_SERVER = 106
ERR_CODE_SET_REST_SERVER_HOST_INVALID_HOST = 107
ERR_CODE_SET_REST_SERVER_HOST_INVALID_PORT = 108
ERR_MONGO_DB_CONN_FAILED = 109
ERR_INSERTING_MONGO_DOCUMENT=110
ERR_ACCESING_MONGO_DB_COLLECTION=111
ERR_UPDATING_MONGO_COLLECTION=112
ERR_MONGO_DOCUMENT_ALEADY_EXISTS=113
ERR_DOCUMENT_DOES_NOT_EXIST=114
ERR_MANDATORY_PARAMETER_MISSING=115
ERR_API_JOBREQUESTREST_FAILED_TO_FETCH_DATA = 116
ERR_RBMQ_MESSAGE_DELIVERY_FAILED = 117
ERR_EXECUTING_MSSQL_DB_QUERY = 118
ERR_MSSQL_DB_CONN_FAILED = 119
ERR_FUNCTIONALITY_NOT_SUPPORTED = 120



SingleErrorMessages = {
        ERR_CODE_INVALID_WORKING_FOLDER_PATH_PROVIDED : 'The path {0} does not exist. Cannot create working folder.',
        ERR_CODE_CANNOT_CREATE_WORKING_FOLDER_PATH: 'Cannot create working folder path at {0}. Error Details: {1}' ,
        ERR_CODE_REST_SERVER_WORKING_FOLDER_CREATE_FAILURE : 'Error while creating working folder for REST Server. Details: {0}',
        ERR_CODE_REST_SERVER_NOT_RUNNING : 'REST server is not running',
        ERR_CODE_REST_SERVER_ALREADY_RUNNING : 'An instance of REST Server already running. Please make sure the instance is shutdown.',
        ERR_CODE_REST_SERVER_SHUTDOWN_REQUEST_FAILED : 'Cannot post shutdown request on the rest server. Error details: {0}',
        ERR_CODE_REST_SERVER_SHUTDOWN_REQUEST_TIMEDOUT : 'The REST server state file still exists after {0} seconds. REST server seems to have failed to shutdown',
        ERR_CODE_ERROR_WHILE_STARTING_REST_SERVER : 'Error while launching REST server. Details: {0}',
        ERR_CODE_SET_REST_SERVER_HOST_INVALID_HOST : 'Invalid value {0} provided for REST server host.',
        ERR_CODE_SET_REST_SERVER_HOST_INVALID_PORT : 'Invalid value {0} provided for REST server port.',
        ERR_MONGO_DB_CONN_FAILED : 'Unable to connect to MongoServer. Check if MongoServer {0}:{1} is active',   
        ERR_INSERTING_MONGO_DOCUMENT: 'Error inserting mongo document for collection {0} with exception message {1}',
        ERR_ACCESING_MONGO_DB_COLLECTION: 'Error accessing mongodb collection {0} with exception message {1}',
        ERR_UPDATING_MONGO_COLLECTION: 'Error updating mongodb collection {0} with _id{1}',
        ERR_MONGO_DOCUMENT_ALEADY_EXISTS : 'Error mongodb document already exists for collection {0} with _id {1}',
        ERR_DOCUMENT_DOES_NOT_EXIST: 'Error mongodb document does not exists in collection {0} with _id {1}',
        ERR_MANDATORY_PARAMETER_MISSING : 'Mandatory parameter(s) - {0} missing.',
        ERR_API_JOBREQUESTREST_FAILED_TO_FETCH_DATA: 'JobRequest Failed to fetch build and test details {0}',
        ERR_RBMQ_MESSAGE_DELIVERY_FAILED: 'Failed to deliver the message to the rabbitmq queue {0}',
        ERR_EXECUTING_MSSQL_DB_QUERY : 'Failed to execute mssql query {0}',
        ERR_MSSQL_DB_CONN_FAILED : 'Unable to connect to MSSQL Server. Check if MSSQL Server {0} and DB {1} is active',
    }
