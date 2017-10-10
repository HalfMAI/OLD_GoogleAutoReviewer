[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=5476a2f8-cdef-46ea-a69a-68550502ab3f
Description=BindAcc
Enable=1
AutoRun=0
[Repeat]
Type=1
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]
Dim g_ScreenX, g_ScreenY
g_ScreenX = Plugin.Sys.GetScRX()
g_ScreenY = Plugin.Sys.GetScRY()

Dim delatNum
delatNum = 5

Dim g_ProjectFloder, g_PicFloder, g_FileFloder
g_ProjectFloder = "C:\_googleRush\_accountBind"
g_PicFloder =  g_ProjectFloder & "\pic"
g_FileFloder = g_ProjectFloder & "\..\syncFiles"

Dim g_AccountTxt, g_BindAccTxt
g_AccountTxt = g_FileFloder & "\acc.txt"
g_BindAccTxt = g_FileFloder & "\bindAcc.txt"

Dim g_Hwnd
Dim g_retX,g_retY

Dim g_Acc, g_Pw

Dim g_kpzsLauncher, g_kpzsQuiter
g_kpzsLauncher = "kpbs926A-StartLauncher.exe"
g_kpzsQuiter = "kpbs926A-Quit.exe"
UserVar kpzsPath="C:\Program Files (x86)\kpzs\bin\bsEmulator\0926\bsEmulator" "kpzs\bin\bsEmulator\0926\bsEmulator"

UserVar isDisplayConsole = "0" "Is display Console? 0 for no, 1 for yes"

//Script Start
/************************************************/
Call Plugin.Console.Close()
Delay 3000

If isDisplayConsole = "1" Then
	Call Plugin.Console.Open()
End If
Call TraceToConsole("-----------------Script Start---------------")

Call CheckIsMuOpend

While Plugin.File.IsFileExist(g_AccountTxt) = False
	//if the file not exist, wait
	Call TraceToConsole("waiting AccountTxt the File...")
	Call TraceToConsole("path:" & g_AccountTxt)
	Delay 5000
Wend

If Plugin.File.IsFileExist(g_BindAccTxt) = False
	Call MyCreateFile(g_BindAccTxt)
End If	

Call readAccFileAndGetAccPw(g_AccountTxt)

Call ResetDeviceSetting
Call CloseLocationTrack
Call BindPlayAcc

//delete the bind acc
Call Lib.文件.删除指定行文本内容(g_AccountTxt, 1)
Call Lib.文件.删除指定行文本内容(g_AccountTxt, 1)

Call TraceToConsole("@-----Finish bind accout : " & g_Acc)
Call WriteStrAtTheEnd(g_BindAccTxt, g_Acc)

Call MyScriptEnd
/************************************************/
//Script end

Sub OnScriptExit()
	Call MyScriptEnd
End Sub

Sub MyScriptEnd	
	Call Plugin.Console.Close()
	
	Delay 3000
End Sub

Sub CheckIsMuOpend
	Call FindMuWinHwnd
	Call TraceToConsole("**Script Starting:" & g_Hwnd)
	If g_Hwnd = "" Then 
		Call ExceptionAndLog("can't find Mu, please check the MU!", False)
		Call openMu
	End If
End Sub

Sub ResetDeviceSetting	
	//set the pos
	Call ResetWindowsPos

	Dim tmp00X, tmp00Y
		
	For 5
		tmpHwnd = Plugin.Window.Search("引擎设置")
		If tmpHwnd = "" Then 
			//open muManager setting
			Call FindPicOnScreenWaitUntilFound("muDevOption.bmp", True, 10, True)
		Else 
			tmpHwnd = Split(tmpHwnd, "|", - 1 )(0)
			Call Plugin.Window.Top(tmpHwnd, 0)
			Call Plugin.Window.Top(tmpHwnd, 1)
			Exit For	
		End If
		Delay 3000
	Next
	
	//Reset Selection
	Call FindPicOnScreenWaitUntilFound("muDevOption_ResetSelection.bmp", True, 10, True)
	
	//clear the Data
	Call FindPicOnScreenWaitUntilFound("muDevOption_DataManager.bmp", True, 10, True)
	Call FindPicOnScreenWaitUntilFound("muDevOption_DataClear.bmp", True, 10, True)
	Call FindPicOnScreenWaitUntilFound("muDevOption_DataClaer_OK.bmp", True, 10, True)
	Delay 3000
//	Call FindPicOnScreenWaitUntilFound("muDevOption_RestartOK0.bmp", True, 10, False)	
	Call FindPicOnScreenWaitUntilFound("muDevOption_RestartOK.bmp", True, 10, True)
		
	Delay 10000	//wait the reboot init
	
	//Close the windows
	Call FindPicOnScreenWaitUntilFound("muDevOption_closeMuDevOption.bmp", True, 10, False)
	
	//wait the emu loaing
	Call WaitForEmuInit
	
	For 5
		tmpHwnd = Plugin.Window.Search("引擎设置")
		If tmpHwnd = "" Then 
			//open muManager setting
			Call FindPicOnScreenWaitUntilFound("muDevOption.bmp", True, 10, True)
		Else 
			tmpHwnd = Split(tmpHwnd, "|", - 1 )(0)
			Call Plugin.Window.Top(tmpHwnd, 0)
			Call Plugin.Window.Top(tmpHwnd, 1)
			Exit For	
		End If
		Delay 3000
	Next
	
	
	//Reset Selection
	Call FindPicOnScreenWaitUntilFound("muDevOption_ResetSelection.bmp", True, 10, True)
	
	//go to the device setting
	Call FindPicOnScreenWaitUntilFound("muDevOption_DevChange.bmp", True, 10, True)	
	
	//GUID gen
	Call FindPicOnScreenWaitUntilFound("muDevOption_Gen.bmp", True, 10, True)
	//save the ref point
	tmp00X = g_retX
	tmp00Y = g_retY
	
	//GUID write
	Call FindPicWaitUntilFound(tmp00X + delatNum, tmp00Y - delatNum, g_ScreenX, g_ScreenY, "muDevOption_Write.bmp", True, 10, True)
	Call FindPicOnScreenWaitUntilFound("muDevOption_OK.bmp", True, 10, True)
	
	//Device gen
	Call FindPicWaitUntilFound(tmp00X - delatNum, tmp00Y + delatNum , g_ScreenX, g_ScreenY, "muDevOption_Gen.bmp", True, 10, True)
	//save the ref point
	tmp00X = g_retX
	tmp00Y = g_retY
	
	//Device write
	Call FindPicWaitUntilFound(tmp00X + delatNum, tmp00Y - delatNum, g_ScreenX, g_ScreenY, "muDevOption_Write.bmp", True, 10, True)
	Call FindPicOnScreenWaitUntilFound("muDevOption_RestartOK.bmp", True, 10, True)
	
	Delay 10000	//wait the reboot init
	
	//Close the windows
	Call FindPicOnScreenWaitUntilFound("muDevOption_closeMuDevOption.bmp", True, 10, True)
	
	//WaitForEmuInit
	Call WaitForEmuInit
End Sub

Sub BindPlayAcc

	Dim retryTime
	retryTime = 0
	
	Rem resetBindSub
	
	//set the pos
	Call ResetWindowsPos

	For 8		
		//Back 8 time to reset
		Call FindPicOnScreenWaitUntilFound("mu_Back.bmp", True, 1, True)
	Next
		
	//open home page
	Call FindPicOnScreenWaitUntilFound("mu_OpenHomePage.bmp", True, 10, False)
	
	Call FindPicOnScreenWaitUntilFound("check_PressedHome.bmp", False, 10, False)
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	
	//open PlayStore
	Call FindPicOnScreenWaitUntilFound("mu_OpenPlayStore.bmp", True, 10, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	Delay 1000	//wait the animation
		
	//exiting Acc
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_ExitAcc.bmp", True, 10, False)
	If g_retX <= 0 Or g_retY <= 0 Then 		
		//check is already Bind
		Call FindPicOnScreenWaitUntilFound("mu_PlayStore_GooglePlayConfirm.bmp", True, 10, False)
		If g_retX > 0 And g_retY > 0 Then 
			Delay 3000
			Exit Sub
		End If
			
		Call FindPicOnScreenWaitUntilFound("check_BindAccEnd.bmp", False, 10, False)	
		If g_retX > 0 And g_retY > 0 Then 
			Exit Sub
		Else
			Goto resetBindSub		//GOTO RESET
		End If
	End If
	
	Call FindPicOnScreenWaitUntilFound("check_AccInput.bmp", False, 10, False)
	If g_retX <= 0 Or g_retY <= 0 Then 
		//wait for bind	
		Call FindPicOnScreenWaitUntilFound("check_AccInput.bmp", False, 10, False)
		If g_retX <= 0 Or g_retY <= 0 Then 
			Goto resetBindSub		//GOTO RESET
		End If
	End If
	
	Call TraceToConsole("current Account:" & g_Acc)
	Call TraceToConsole("current Pw:" & g_Pw)
		
	//input Acc
	Call InputText(g_Acc)	
	//input pw	
	KeyPress "Tab", 1
	Delay 1000
	
	Call InputText(g_Pw)
	Delay 1000//wait the Input
		
	//next
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_Next.bmp", True, 5, False)
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	Delay 500	//wait the animation
				
	//rule confirm
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_RulesConfirm.bmp", True, 15, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	Delay 1500	//wait the animation
			
	Call FindPicOnScreenWaitUntilFound("check_PasswordOK.bmp", False, 10, False)			
	If g_retX <= 0 Or g_retY <= 0 Then 
		//check wrong password
		Call FindPicOnScreenWaitUntilFound("check_PasswordError.bmp", False, 10, False)
		If g_retX > 0 And g_retY > 0 Then 
			If retryTime > 3 Then 
				tmpLogPath = g_FileFloder & "\wrongPassword.txt"
				If Plugin.File.ExistFile(tmpLogPath) = False Then
					Call MyCreateFile(tmpLogPath)
				End If
				Call WriteStrAtTheEnd(tmpLogPath, g_Acc)
				
				//delete the wrong acc
				Call Lib.文件.删除指定行文本内容(g_AccountTxt, 1)
				Call Lib.文件.删除指定行文本内容(g_AccountTxt, 1)
				Call MyRestartScript
			Else 
				retryTime = retryTime + 1
				Goto resetBindSub
			End If		
		End If
	End If
	
	//next
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_Next.bmp", True, 15, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	Delay 500	//wait the animation
	
	//skip payment
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_SkipPaymentSetting.bmp", True, 20, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If	
	Delay 500	//wait the animation
	
	//last confirm	
	Call FindPicOnScreenWaitUntilFound("mu_PlayStore_GooglePlayConfirm.bmp", True, 30, False)
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetBindSub		//GOTO RESET
	End If
	
	Delay 3000
End Sub

Sub CloseLocationTrack
	
	Rem resetSettionLoaction
	
	Call TraceToConsole("Going to the Location tracking~")
	//set the pos
	Call ResetWindowsPos

	For 5		
		Call FindPicOnScreenWaitUntilFound("mu_Back.bmp", True, 1, True)
	Next
	
	//open home page
	Call FindPicOnScreenWaitUntilFound("mu_OpenHomePage.bmp", True, 10, False)
	
	//open Option	
	Call FindPicOnScreenWaitUntilFound("mu_Location_Open.bmp", True, 10, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetSettionLoaction		//GOTO RESET
	End If
	
	//open advance	
	Call FindPicOnScreenWaitUntilFound("mu_Location_Advance.bmp", True, 10, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetSettionLoaction		//GOTO RESET
	End If
		
	//open location setting	
	Call FindPicOnScreenWaitUntilFound("mu_Location_LocationSetting.bmp", True, 10, False)	
	If g_retX <= 0 Or g_retY <= 0 Then 
		Goto resetSettionLoaction		//GOTO RESET
	End If
	
	//turn off location tracking	
	Call FindPicOnScreenWaitUntilFound("mu_Location_LocationSetOff.bmp", True, 10, True)
		
	Call TraceToConsole("Closed the Location tracking~")
	
	Delay 1000
End Sub

Function InputText(str)
	Call lib.键盘.KeyList(str, 0, 100)
End Function

Function TraceToConsole(str)
	tmpLogPath = g_ProjectFloder & "\normalLog.txt"
	If Plugin.File.ExistFile(tmpLogPath) = False Then
		Call MyCreateFile(tmpLogPath)
	End If
	Call WriteStrAtTheEnd(tmpLogPath, Now & " " & str)

	If isDisplayConsole = "1" Then
		Plugin.Console.WriteLine (str & vbcrlf)
	End If	
End Function

Function MyRestartScript
	Call MyScriptEnd
	Delay 1000
	RestartScript
End Function

Function readAccFileAndGetAccPw(filePath)
	tmpText = Plugin.File.ReadFileEx(filePath)  
	If tmpText = "" Then 
		Call ExceptionAndLog("There is No more account!!!!!!!!!!!!!!!!!!!!!!!!", True)
	Else 
		tmpArr = Split(tmpText, "|")
	End If 
	
	Call TraceToConsole(tmpText)
	
	g_Acc = tmpArr(0)
	g_Pw = tmpArr(1)	
	
	Call TraceToConsole("current Account:" & g_Acc)
	Call TraceToConsole("current Pw:" & g_Pw)
End Function

//Find the hwnd
Function FindMuWinHwnd	
	g_Hwnd = Plugin.Window.Search("靠谱助手 -- Powered by BlueStacks")
	If g_Hwnd = "" Then 
	Else 
		g_Hwnd = Split(g_Hwnd, "|", - 1 )(0)
	End If 
	Call TraceToConsole("Current hwnd: " & g_Hwnd)
End Function

Function openMu
	Call RunApp(kpzsPath & "\" & g_kpzsQuiter)
	Delay 1000	
	Call RunApp(kpzsPath & "\" & g_kpzsLauncher)
		
	Call WaitForEmuInit()	
End Function

//reset the windows pos
Function ResetWindowsPos
	Call FindMuWinHwnd
	If g_Hwnd = "" Then 
	Else 
		Call TraceToConsole("Bring up the Windows")
		Call Plugin.Window.Top(g_Hwnd, 0)
		Call Plugin.Window.Top(g_Hwnd, 1)
		Call Plugin.Window.Move(g_Hwnd, 1, 1)
	End If	
	Delay 500	//give some Delay
End Function

//move and click at somePoint
Function MoveAndClick(mx, my)
    MoveTo mx + delatNum, my + delatNum
    //LeftClick 1
    LeftDown 1
    Delay 150
    LeftUp 1    
    Delay 100
End Function

Function FindPicWaitUntilFound(sX, sY, eX, eY, picPath, isClick, waitTime, isFailToEnd)
    Call TraceToConsole("Finding : " & picPath)
    delayTime = 1000
	Dim loopTime
	loopTime = waitTime * 1000 \ delayTime //int Div
	picPath = g_PicFloder & "\" & picPath	
	loopTime = loopTime + 1
	
	For loopTime		
    	FindPic sX, sY, eX, eY, picPath, 0.99, retX, retY
    	
    	If retX > 0 And retY > 0 Then
    		If isClick = True Then
    			Call MoveAndClick(retX, retY)
    		End If    		
    		Call TraceToConsole("Found pic: " & picPath & "_" & retX & "," & retY)
    		Delay 500
    		Exit For
    	Else 
			MoveTo g_ScreenX, 20
    	End If
    	Delay delayTime
    	
		If isDisplayConsole = "1" Then
			Plugin.Console.WriteLine ("retry for the pic: " & picPath & vbcrlf)
		End If	
	Next
	
	//save as G_
	g_retX = retX
	g_retY = retY

    If retX <= 0 Or retY <= 0 Then 
        Call ExceptionAndLog("Can't Find Pic" & picPath, isFailToEnd)
    End If
End Function

Function FindPicOnScreenWaitUntilFound(picPath, isClick, waitTime, isFailToEnd)
	Call FindPicWaitUntilFound(0,0,g_ScreenX,g_ScreenY, picPath, isClick, waitTime, isFailToEnd)
End Function

Function WaitForEmuInit
	For 30	
		//set the pos
		Call ResetWindowsPos
		
		Call TraceToConsole("wait Looping")
		Call FindPicOnScreenWaitUntilFound("muIsLoadingMark.bmp", False, 1, False)
		If g_retX > 0 And g_retY > 0 Then 
			Call TraceToConsole("emu is booting, wait for it")
			Delay 5000
		Else 
			Call FindPicOnScreenWaitUntilFound("muIsLoadingEndMark.bmp", False, 5, False)
			If g_retX > 0 And g_retY > 0 Then 
				Call TraceToConsole("emu is booted, end wating")
				Call FindPicOnScreenWaitUntilFound("muDevOption_OK1.bmp", True, 2, False)
				Exit Function
				Exit For
			End If
			
			Delay 5000
		End If
	Next
	
	Call ExceptionAndLog("Can't boot the emu", True)
End Function

Function ExceptionAndLog(exceptionLog, isRestartScript)
	Call TraceToConsole(exceptionLog)
	
	tmpFilePath = g_ProjectFloder & "\exception.log"
	If Plugin.File.ExistFile(tmpFilePath) = False Then 
		Call MyCreateFile(tmpFilePath)
	End If
		
	Call WriteStrAtTheEnd(tmpFilePath, Now & " " & exceptionLog)
		
	If isRestartScript = True Then 
		tmpRestartFilePath = g_ProjectFloder & "\restartError.log"
		If Plugin.File.ExistFile(tmpRestartFilePath) = False Then 
			Call MyCreateFile(tmpRestartFilePath)
		End If
		
		Call WriteStrAtTheEnd(tmpRestartFilePath, Now & " " & exceptionLog)
		
		Call MyRestartScript
	End If
End Function

Function MyCreateFile(path)	
	handle = Plugin.File.OpenFile(path)   
	Call Plugin.File.WriteFile(handle, "")
	Call Plugin.File.CloseFile(handle)
	
	Delay 500
End Function

Function WriteStrAtTheEnd(path, str)	
	fileLen = Plugin.File.GetFileLength(path)
	handle = Plugin.File.OpenFile(path)   
	Call Plugin.File.SeekFile(handle, fileLen)   
	Call Plugin.File.WriteLine(handle, str)
	Call Plugin.File.CloseFile(handle)
	
	Delay 500
End Function
