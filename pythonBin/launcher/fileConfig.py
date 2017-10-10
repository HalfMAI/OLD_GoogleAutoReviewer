import os
from ConfigParser import SafeConfigParser

def __ConfigInit():
    tmpParentDic = os.path.join(ConfigReader.curProjectPath, os.path.pardir)
    ConfigReader.readConfig(os.path.join(tmpParentDic, "fileConf.ini"))
    
class ConfigReader:
    curProjectPath = os.path.split(os.path.realpath(__file__))[0]
    accFilePath = ""
    bindFilePath = ""
    reportedFilePath = ""
    wrongPasswordFilePath = ""
    pythonLogPath = ""
    revieweTextPath = ""
    
    getUnbindAccURL = ""
    postAccStatusURL = ""
    getReviewTextURL = ""
    
    packageName = ''
    gameCode = ''
    language = ''
        
    @staticmethod
    def readConfig(confPath):
        tmpParser = SafeConfigParser()
        tmpParser.read(confPath)
        
        fileFloderPath = tmpParser.get('FileConfig', 'accountFilePath')
        
        ConfigReader.accFilePath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'accountTxt'))
        ConfigReader.bindFilePath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'bindTxt'))
        ConfigReader.reportedFilePath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'reportedTxt'))
        ConfigReader.wrongPasswordFilePath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'wrongPasswordTxt'))
        ConfigReader.pythonLogPath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'pythonLog'))
        ConfigReader.revieweTextPath = os.path.join(fileFloderPath, tmpParser.get('FileConfig', 'reviewTextTxt'))
        
        ConfigReader.getUnbindAccURL = tmpParser.get('URLConfig', 'getUnbindAccURL')
        ConfigReader.postAccStatusURL = tmpParser.get('URLConfig', 'postAccStatusURL')
        ConfigReader.getReviewTextURL = tmpParser.get('URLConfig', 'getReviewTextURL')
                
        ConfigReader.packageName = tmpParser.get('ReviewerConfig', 'packageName')
        ConfigReader.gameCode = tmpParser.get('ReviewerConfig', 'gameCode')
        ConfigReader.language = tmpParser.get('ReviewerConfig', 'language')
     
#run
__ConfigInit()
print "#run __ConfigInit()"