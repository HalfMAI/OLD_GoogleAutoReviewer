import urllib2,json,sys,base64
from fileConfig import ConfigReader
from myLoger import myLoger

def __httpConfig():
    urllib2.socket.setdefaulttimeout(30)

#call
__httpConfig()

class HttpGetData:    
    @staticmethod
    def startRequest(link, dicPra):        
        if dicPra != None: 
            for i,v in enumerate(dicPra):  
                v = v.rstrip()
                link = link + ("?" if i == 0 else "&")
                link = link + str(v) + "=" + dicPra[str(v)]
            pass
        myLoger("-----Requesting Link: " + str(link))
        
        retData = None
        try:
            requestData = urllib2.urlopen(link).read()
            retData = json.loads(requestData)
        except:
            myLoger("==========================!!!!!!!!!!Unexpected error:", sys.exc_info()[0])
            retData = None
        myLoger("-----Responsed Data: " + str(retData))
        return retData
        
class ServerConnection:
    _myEncodeKey = "e8"
    
    @staticmethod
    def getUnbindAcc():
        retData = {}      #{ "acc" : "", "pwd" : "" }
        
        tmpRequestUrl = ConfigReader.getUnbindAccURL
        tmpRequestParams = None
        
        tmpRequestedDic = HttpGetData.startRequest(tmpRequestUrl, tmpRequestParams)
        
        if tmpRequestedDic != None:
            tmpCode = tmpRequestedDic["code"]
            
            if tmpCode == "1000":         
                tmpData = tmpRequestedDic["data"]            
                tmpStr = base64.b64decode(tmpData)
                tmpStr = tmpStr[len(ServerConnection._myEncodeKey):]
                tmpStr = base64.b64decode(tmpStr)
                                
                tmpAcc = tmpStr.split('|')[0]
                tmpPw = tmpStr.split('|')[1]
                # tmpAcc = tmpData["username"]
                # tmpPw = tmpData["password"]
                
                
                myLoger(tmpAcc + tmpPw)
                
                retData["acc"] = tmpAcc
                retData["pwd"] = tmpPw
            else:
                retData = None
                pass #TODO post or retry, somthing like that
        return retData
        
    @staticmethod
    def postAccStatus(acc, accStatus, gameCode):
        retStatus = False  
        
        #TODO encode the acc
        
        tmpRequestUrl = ConfigReader.postAccStatusURL
        tmpRequestParams = {
            "username"  :   acc,
            "mode"      :   accStatus
        }
        
        if accStatus == "reviewed":
            tmpRequestParams["gameCode"] = gameCode
        
        tmpRequestedDic = HttpGetData.startRequest(tmpRequestUrl, tmpRequestParams)        
        
        if tmpRequestedDic != None:
            tmpCode = tmpRequestedDic["code"]
            if tmpCode == "1000":            
                #TODO other ?
                retStatus = True
            else:
                retStatus = False
                pass #TODO post or retry, somthing like that
        return retStatus
        
    @staticmethod
    def getReviewText(gameCode, language):
        retData =  {}     #{ "reviewText" : "", "isNewGP" : "", "acc" : "", "pwd" : ""}
                
        tmpRequestUrl = ConfigReader.getReviewTextURL
        tmpRequestParams = {
            "language"  :   language ,
            "gameCode"  :   gameCode
        }
        
        tmpRequestedDic = HttpGetData.startRequest(tmpRequestUrl, tmpRequestParams)        
        
        if tmpRequestedDic != None:
            tmpCode = tmpRequestedDic["code"]
            
            if tmpCode == "1000":   
                tmpData = tmpRequestedDic["data"]
                
                tmpStr = base64.b64decode(tmpData)
                tmpStr = tmpStr[len(ServerConnection._myEncodeKey):]
                tmpStr = base64.b64decode(tmpStr)
                
                tmpAcc = tmpStr.split('|')[0]
                tmpPw = tmpStr.split('|')[1]
                # tmpAcc = tmpData["username"]
                # tmpPw = tmpData["password"]
                
                tmpReviewTextData = tmpRequestedDic["reviewText"]
                retData["reviewText"] = tmpReviewTextData["content"]
                retData["isNewGP"] = tmpReviewTextData["isNewGP"]
                retData["acc"] = tmpAcc
                retData["pwd"] = tmpPw
            else:
                retData = None
                pass #TODO post or retry, somthing like that
        return retData
      