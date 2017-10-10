from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from datetime import datetime
from time import sleep
from myLoger import myLoger
from fileConfig import ConfigReader

from serverConnection import ServerConnection

def _startReview():
    tmpPackageName = ConfigReader.packageName
    tmpGameCode = ConfigReader.gameCode
    tmpLanguage = ConfigReader.language
    
    #request the data
    myLoger("Start Requesting Data")
    retDic = ServerConnection.getReviewText(tmpGameCode, tmpLanguage)
        
    tmpEmail = retDic["acc"] 
    tmpPassword = retDic["pwd"]        
    tmpReviewText = retDic["reviewText"]
    tmpIsNewGP = retDic["isNewGP"]
    
    reviewer = Reviewer(tmpEmail, tmpPassword, tmpGameCode, tmpPackageName, tmpReviewText) 
    # reviewer = Reviewer("xiaoming000060@gmail.com", "xiaoming001", tmpGameCode, tmpPackageName, tmpReviewText)        
    myLoger(
        'Start Proccessing with PackageName: ' + tmpPackageName + '\n' +
        'GameCode: ' + tmpGameCode + '\n' + 
        'Language: ' + tmpLanguage + '\n' +
        'Account: ' + tmpEmail + '\n' +
        'Passwd: ' + tmpPassword
    )
    
    try:
        reviewer.startLoginGoogleAcc()
        
        myLoger("tmpIsNewGP:" + str(tmpIsNewGP))    
        if str(tmpIsNewGP) == '0': 
            reviewer.startRegistGooglePlus()
                
        reviewer.startReviewAndSumit()        
        myLoger('-----------------submit OK : ' + tmpEmail + '; ' + 'packageName:' + tmpPackageName)
    finally:
        reviewer.endReviewing()

class Reviewer:
    loginEmailXpath = '//*[@id="Email"]'
    loginPasswordXpath = '//*[@id="Passwd"]'
        
    installBtnXpath = '//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/span/span/button'
    installedBtnXpath = '//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/span/span/span/button[2]'
    
    installToPhoneXpath = '//*[@id="purchase-ok-button"]'
    installConfirmXpath = '//*[@id="close-dialog-button"]'
    
    openReviewBtnXpath = '//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/button[1]'
    openReviewedBtnXpah = '//*[@id="id-edit-review-button"]'
    
    reviewNewGplusConfirmCSSPath = 'body > div.modal-dialog.review-widget-dialog > div > div > div > div.details-wrapper.apps > div > div > div.review-help.id-gpr-onboard > div.review-panel-content > div:nth-child(3) > div > button'
    
    reviewStarCSSPath = 'body > div.modal-dialog.review-widget-dialog > div > div > div > div.details-wrapper.apps > div > div > div.write-review-panel > div > div.review-main > div.review-right-col > div.review-row.star-rating-row-desktop > div > div > div.medium-star-material > div.star-rating-aria > button.fifth-star'
    reviewTextCSSPath = 'body > div.modal-dialog.review-widget-dialog > div > div > div > div.details-wrapper.apps > div > div > div.write-review-panel > div > div.review-main > div.review-right-col > div:nth-child(2) > div > textarea'
    reviewSumitCSSPath = 'body > div.modal-dialog.review-widget-dialog > div > div > div > div.details-wrapper.apps > div > div > div.write-review-panel > div > div.review-main > div.review-right-col > div.review-row.review-action-buttons-row > div:nth-child(1) > button'
    
    def __init__(self, email, pwd, gameCode, packageName, reviewTxt):
        self.gameCode = gameCode
        self.email = email
        self.password = pwd
        self.packageName = packageName
        self.reviewText = reviewTxt
        self.storeLink = 'https://play.google.com/store/apps/details?id=' + packageName
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Remote("http://localhost:4444/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT) 
    
    def waitElemFormXpath(self, driver, xpath):
        elem = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return elem
    
    def waitElemFormCssPath(self, driver, cssPath):
        elem = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssPath)))
        return elem
    
    def elemFill(self, elem, val, isPressedReturn):
        elem.send_keys(val)
        if isPressedReturn:
            elem.send_keys(Keys.RETURN)
    
    def startLoginGoogleAcc(self):
        myLoger("StartLoginGoogleAcc..., going to accounts page")
        self.driver.get("https://accounts.google.com")
        
        myLoger("StartLoginGoogleAcc..., filling account")
        # fill account
        elem = self.waitElemFormXpath(self.driver, self.loginEmailXpath) 
        self.elemFill(elem, self.email, True)
        
        myLoger("StartLoginGoogleAcc..., filling password")
        # fill password 
        elem = self.waitElemFormXpath(self.driver, self.loginPasswordXpath)
        self.elemFill(elem, self.password, True)
        
        #wait for the session saved
        sleep(1)
    
    def _pressTheInstallBtn(self):
        myLoger("_pressTheInstallBtn..., checking the install button")
        try:           
            installedBtn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.installedBtnXpath)))
            if installedBtn.is_displayed():
                myLoger("_pressTheInstallBtn..., already installed")
                installedBtn.click()
                myLoger('already installed')
        except Exception, e:
            myLoger("_pressTheInstallBtn..., New install") 
            myLoger("_pressTheInstallBtn..., Let's intall it!")
            print e
            self.waitElemFormXpath(self.driver, self.installBtnXpath).click()
    
    def startReviewAndSumit(self):
        myLoger("startReviewAndSumit..., Going to the Store:" + self.storeLink)
        self.driver.get(self.storeLink)
        
        # pressed the install button
        self._pressTheInstallBtn()
               
        try:
            myLoger("startReviewAndSumit..., intall to the phone")
            #intall to the phone
            self.waitElemFormXpath(self.driver, self.installToPhoneXpath).click()
        except:
            self._pressTheInstallBtn()
        
        myLoger("startReviewAndSumit..., confirm btn")
        #confirm btn
        self.waitElemFormXpath(self.driver, self.installConfirmXpath).click()
        
        self.driver.get(self.storeLink)
        
        myLoger("startReviewAndSumit..., review btn")
        #review
        try:            
            self.waitElemFormXpath(self.driver, self.openReviewBtnXpath).click()
        except:
            self.waitElemFormXpath(self.driver, self.openReviewedBtnXpah).click()
        
        myLoger("startReviewAndSumit..., get the reviewLink")
        #get the reviewLink
        submitreviewLink = self.waitElemFormXpath(self.driver, '//*[@id="glass-content"]').find_elements_by_tag_name('iframe')[0].get_attribute('src')
        
        myLoger("startReviewAndSumit..., get the reviewLink")
        self.driver.get(submitreviewLink)
        
        try:
            myLoger("startReviewAndSumit..., Checking is New GooglePlus?")
            newGpConfirm = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.reviewNewGplusConfirmCSSPath)))
            if newGpConfirm.is_displayed():
                myLoger("startReviewAndSumit..., YES, you are New GooglePlus, registing")
                newGpConfirm.click()
        except Exception, e:
            myLoger("startReviewAndSumit..., No, not new Google Plus")
            myLoger("startReviewAndSumit..., Exception : " + str(e))
        
        
        myLoger("startReviewAndSumit..., clicking the reviewStar")
        #reviewStar
        self.waitElemFormCssPath(self.driver, self.reviewStarCSSPath).click()
        
        myLoger("startReviewAndSumit..., inputing reviewText: " + self.reviewText.encode('utf-8'))
        #reviewText
        self.elemFill(self.waitElemFormCssPath(self.driver, self.reviewTextCSSPath), self.reviewText, False)
        
        myLoger("startReviewAndSumit..., submiting Review")
        self.waitElemFormCssPath(self.driver, self.reviewSumitCSSPath).click()
        
        tmpVal = self.email.strip()
        ServerConnection.postAccStatus(tmpVal, "reviewed", self.gameCode)
        
        with open(ConfigReader.reportedFilePath, 'a+') as tmpFile:
            myLoger("Saving Log " + "reviewed" + " Acc: " + tmpVal)
            tmpFile.write(str(datetime.now()) + "   " + "=reviewed=" + "    " + tmpVal + " Code:" + self.gameCode + "     \n")
            tmpFile.close()
        
        sleep(3)
        self.endReviewing()
        
    def startRegistGooglePlus(self):
        myLoger("startRegistGooglePlus..., Going to regist the GooglePlus")
        self.driver.get("https://plus.google.com")
        
        # self.waitElemFormXpath(self.driver, '//*[@id="content"]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div').click()
        myLoger("startRegistGooglePlus..., registing GP")
        # registGP
        
        myLoger("startRegistGooglePlus..., Checking is New GooglePlus?")
        try:
            theGPConfrimBtn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[4]/div/div')))
            if theGPConfrimBtn.is_displayed():
                myLoger("startRegistGooglePlus..., Need to regist GP registing GP")
                theGPConfrimBtn.click()                
        except Exception, e:
            myLoger("startRegistGooglePlus..., no Need to regist GP, go to store~")
            myLoger("startRegistGooglePlus..., Exception : " + str(e))
        
        try:                
            theGPConfrimBtnNextBtn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div[3]/button[1]')))  
            if theGPConfrimBtnNextBtn.is_displayed():
                myLoger("startRegistGooglePlus..., Bad name registing GP")
                theGPConfrimBtnNextBtn.click()     
        except Exception, e:
            myLoger("startRegistGooglePlus..., no Need to Bad name registing GP regist GP, go to store~")
            myLoger("startRegistGooglePlus..., Bad name registing GP Exception : " + str(e))
        
        #wait the session
        sleep(5)
        
    def endReviewing(self):    
        try:    
            self.driver.quit()
        except:
            pass

if __name__ == '__main__': 
    while 1:              
        myLoger("==============starting a new sesseion~")
        try:
            _startReview()
        except Exception as e:
            myLoger("somethin wrong !!!")
            myLoger(str(e))
        
        sleep(5)
        pass   