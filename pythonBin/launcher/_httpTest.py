from serverConnection import ServerConnection
import sys

def httpTest():
    retDic = ServerConnection.getUnbindAcc()
    print retDic
    
    tmpAcc = retDic["acc"]
    tmpMode = "bind"
    tmpGameCode = 'ddd'
    tmpLanguage = "en_US"
    
    print "-----------------\n"
    
    retStatus = ServerConnection.postAccStatus(tmpAcc, tmpMode, tmpGameCode)
    print retStatus
        
    print "-----------------\n"
    
    retData = ServerConnection.getReviewText(tmpGameCode, tmpLanguage)
    print retData
    
    print "-----------------\n"
    tmpMode = "reviewed"    
    retStatus = ServerConnection.postAccStatus(tmpAcc, tmpMode, tmpGameCode)
    print retStatus

httpTest()