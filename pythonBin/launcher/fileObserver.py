import sys,os,thread,time

from fileConfig import ConfigReader
from datetime import datetime
from serverConnection import ServerConnection
from myLoger import myLoger

class FileObserver:
    checkInterval = 1
    filePath = ""
    def __init__(self, _filePath, interval):
        self.checkInterval = interval
        self.filePath = _filePath
        
    def startObserverAccFile(self):
        thread.start_new_thread(self.__ObserverAccountFile, ())
        
    def startObserverBindFile(self, reportedAccPath):
        thread.start_new_thread(self.__OberverBindFile, (reportedAccPath,))
        
    def startObserverWrongPwdFile(self, reportedAccPath):
        thread.start_new_thread(self.__OberverWrongPwdFile, (reportedAccPath,))
    
    def startObserverReviewTextFile(self, reportedAccPath):        
        thread.start_new_thread(self.__OberverReviewText, ())
    
    def __OberverReviewText(self):
        while 1:
            myLoger("__Obervering ReviewText")   
            
            currentLines = 0
            fileAccArr = []
            
            with open(self.filePath, 'a+') as tmpFile:
                tmpFile.seek(0)
                for i, v in enumerate(tmpFile):
                    tmpVal = v.strip()
                    myLoger("current ReviewText file: " + str(i) + " v: " + str(tmpVal))
                    if tmpVal != "" :
                        currentLines += 1   
                        fileAccArr.append(tmpVal)
                tmpFile.close()
                
                _maxLines = 1
                #get ReviewText
                if currentLines < _maxLines:
                    myLoger("No enough ReviewText, go get ReviewText")
                    retDic = ServerConnection.getReviewText(ConfigReader.gameCode, ConfigReader.language)             
                    if retDic != None:
                        tmpEmail = retDic["acc"] 
                        tmpPassword = retDic["pwd"]        
                        tmpReviewText = retDic["reviewText"]
                        tmpIsNewGP = retDic["isNewGP"]  
                            
                        fileAccArr.append(tmpReviewText)
                        myLoger('Adding ReviewText: ' + tmpReviewText)
                
                        with open(self.filePath, 'w+') as tmpFile:
                            tmpFile.seek(0)                    
                            for i, v in enumerate(fileAccArr):
                                addEnter = '\n'
                                if i > currentLines+1:
                                    addEnter = "" 
                                tmpFile.write(v + addEnter)
                            tmpFile.close()
                else:
                    myLoger("Already have more than 1 ReviewText")                
                tmpFile.close()
            
            time.sleep(self.checkInterval)
    
    def __OberverBindFile(self, reportedAccPath):
        self.__OberverFileAndPost(reportedAccPath, "bind")
        
    def __OberverWrongPwdFile(self, reportedAccPath):
        self.__OberverFileAndPost(reportedAccPath, "pwd_Error")
            
    def __OberverFileAndPost(self, reportedAccPath, modeStr):
        while 1:                
            myLoger("__Obervering " + str(modeStr) + " File: " + self.filePath)  
                  
            currentLines = 0
            
            fileAccArr = []
            with open(self.filePath, 'a+') as tmpFile:
                tmpFile.seek(0)
                currentLines = 0
                for i, v in enumerate(tmpFile):               
                    if v != "" :
                        currentLines += 1     
                        fileAccArr.append(v.strip())
                tmpFile.close()
            
            tmpAccArr = []  
            writeAccArr = []          
            if currentLines > 0:
                myLoger(str(modeStr) + " had something, go and post the server")
                for i, v in enumerate(fileAccArr):
                    myLoger(str(modeStr) + " i:" + str(i) + " v: " + str(v))
                    retStatus = ServerConnection.postAccStatus(v, modeStr, None)                     
                    #................
                    if modeStr == "bind":
                        retStatus = ServerConnection.postAccStatus(v, "reviewed", ConfigReader.gameCode)                     
                    #................
                    if retStatus == True:
                        writeAccArr.append(v)
                        myLoger("posted " + str(modeStr) + " Acc to server: " + v)
                        myLoger("-----------posted " + str(modeStr) + " --------------")
                        #................
                        if modeStr == "bind":
                            myLoger("posted " + "reviewed" + " Acc to server: " + v)
                            myLoger("-----------posted " + "reviewed" + " --------------")                        
                        #................
                    else:
                        tmpAccArr.append(v)
                    
            with open(self.filePath, 'w+') as tmpFile:
                tmpFile.seek(0)
                for i, v in enumerate(tmpAccArr): 
                    myLoger("resolving the fail reported Acc: " + v)
                    tmpFile.write(v + '\n')
                tmpFile.close()
            
            with open(reportedAccPath, 'a+') as tmpFile:
                for i, v in enumerate(writeAccArr): 
                    myLoger("Saving Log " + str(modeStr) + " Acc: " + v)
                    tmpFile.write(str(datetime.now()) + "   " + str(modeStr) + "    " + v + "\n")
                    #................
                    if modeStr == "bind":
                        tmpFile.write(str(datetime.now()) + "   " + "reviewed " + ConfigReader.gameCode + "    " + v + "\n")                 
                    #................
                tmpFile.close()
            time.sleep(self.checkInterval)
                            
    def __ObserverAccountFile(self):
        while 1:                             
            myLoger("__Obervering Account")   
            
            currentLines = 0
            fileAccArr = []
            
            with open(self.filePath, 'a+') as tmpFile:
                tmpFile.seek(0)
                for i, v in enumerate(tmpFile):
                    tmpVal = v.strip()
                    myLoger("current acc file: " + str(i) + " v: " + str(tmpVal))
                    if v != "" :
                        currentLines += 1   
                        fileAccArr.append(tmpVal)
                tmpFile.close()
            
            _maxLines = 20
            #get acc
            if currentLines < _maxLines:
                myLoger("No enough Acc, go get Acc")
                retDic = ServerConnection.getUnbindAcc()        
                if retDic != None:
                    myLoger(retDic)                    
                    addAcc = retDic["acc"].strip()
                    addPw = retDic["pwd"].strip()
                    fileAccArr.append(addAcc)
                    fileAccArr.append(addPw)
                    
                    myLoger('Adding Account: ' + addAcc + ',' + addPw)
            
                    with open(self.filePath, 'w+') as tmpFile:
                        tmpFile.seek(0)                    
                        for i, v in enumerate(fileAccArr):
                            addEnter = '\n'
                            if i > currentLines+2:
                                addEnter = "" 
                            tmpFile.write(v + addEnter)
                        tmpFile.close()
                else:
                    myLoger("Already have more than 5 accounts")                
                tmpFile.close()
                
            time.sleep(self.checkInterval)

#-----------------------------------------


    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    fO_acc = FileObserver(ConfigReader.accFilePath, 300)
    fO_acc.startObserverAccFile()
    
    fO_bind = FileObserver(ConfigReader.bindFilePath, 310)
    fO_bind.startObserverBindFile(ConfigReader.reportedFilePath)
    
    fO_review = FileObserver(ConfigReader.revieweTextPath, 310)
    fO_review.startObserverReviewTextFile(ConfigReader.reportedFilePath)
    
    fO_wrongPwd = FileObserver(ConfigReader.wrongPasswordFilePath, 320)
    fO_wrongPwd.startObserverWrongPwdFile(ConfigReader.reportedFilePath)
    
    while 1:
        time.sleep(300)
        pass