from Handlers.ErrorCodes import * #@UnusedWildImport

class RagapiservicesException(Exception):
    
    def __init__(self, errCode = None, *errMsgParams):
        self._ErrorMsgs = dict()
                
        if SingleErrorMessages:
            self._ErrorMsgs.update(SingleErrorMessages)
            

        self._ErrorCode = None
        self._ErrorMessage = None
            
        if errCode is None:
            return Exception()
            
        if (
            (type(errCode) is str) and
            (errMsgParams is None)
           ):
            return Exception(errCode)
        
        self._ErrorCode = errCode
        self._ErrorMessage = errCode
        if errCode in self._ErrorMsgs:
            self._ErrorMessage = self._ErrorMsgs[self._ErrorCode].format(*errMsgParams)

    def GetErrorCode(self):
        return self._ErrorCode
    
    def GetErrorMessage(self):
        return self._ErrorMessage
    
    def __str__(self):
        if (
            (self._ErrorCode) and
            (self._ErrorMessage)
           ):
            return 'ERROR %s : %s' % (self._ErrorCode, self._ErrorMessage)
        else:
            return 'Undefined exception'
    
    def __repr__(self):
        if (
            (self._ErrorCode) and
            (self._ErrorMessage)
           ):
            return 'ERROR %s : %s' % (self._ErrorCode, self._ErrorMessage)
        else:
            return 'Undefined exception'
    