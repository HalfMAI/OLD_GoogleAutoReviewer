from datetime import datetime
from fileConfig import ConfigReader


def myLoger(logStr):
    resStr = str(datetime.now()) + "   " + str(logStr) + '\n'
    print resStr
    
    with open(ConfigReader.pythonLogPath, 'a+') as tmpFile:
        tmpFile.write(resStr)

myLoger("===============python start===============")