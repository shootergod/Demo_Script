#include <File.au3>
#include <FileConstants.au3>
#include <WinAPIFiles.au3>

#include <Date.au3>

#include <AutoItConstants.au3>

#include <MsgBoxConstants.au3>

#include <WinAPI.au3>

; Press Esc to terminate script,

;~ crtl  : ^
;~ shift : +
;~ alt   : !

;~ WinActivate("[CLASS:Chrome_WidgetWin_1]", "")
Dim $hWnd = WinGetHandle("[CLASS:Chrome_WidgetWin_1]", "")
;~ MsgBox($MB_SYSTEMMODAL, "Info", $hWnd) 
WinActivate($hWnd)
MsgBox($MB_SYSTEMMODAL, "Info", WinActive($hWnd)) 

Exit


Dim $time_str = ""
_GetTimeStr($time_str)

Dim $wd = @ScriptDir
Dim $fn = "Log_ff_"

Dim $fp = $wd & "\" & $fn & $time_str & ".txt"



;~ ------------------------------------------------------------
_PrepareLogFile($fp)

Dim $loop_n = 10
Dim $aFill[$loop_n]
For $i = 0 To 4
    $aFill[$i] = "New Item " & $i + 2
Next
MsgBox($MB_SYSTEMMODAL + $MB_ICONERROR, "Error", UBound($aFill))  


_ArrAppend2Txt($fp, $aFill)


;~ ------------------------------------------------------------
Func _PrepareLogFile($fp)
    If FileExists($fp) Then
        FileDelete($fp)
    EndIf
    FileOpen($fp, $FO_CREATEPATH)
    FileWriteLine($fp, ">>> Record Begin: ")
    FileClose($fp) 
    Return True
EndFunc


;~ ------------------------------------------------------------
Func _ArrAppend2Txt($fp, $arr)
    $file = FileOpen($fp, $FO_APPEND)
    If $file <> -1 Then
        For $i = 0 To UBound($arr) - 1
            If ($arr[$i] <> "") Then
                FileWriteLine($file, $arr[$i])
            EndIf
        Next
        
        FileClose($file)  
    Else  
        MsgBox($MB_SYSTEMMODAL + $MB_ICONERROR, "Error", "无法打开文件。")  
    EndIf
    Return True
EndFunc



;~ ------------------------------------------------------------
Func _StrAppend2Txt($fp, $info)
    $file = FileOpen($fp, $FO_APPEND)
    If $file <> -1 Then
        FileWriteLine($file, $info)  
        FileClose($file)  
    Else  
        MsgBox($MB_SYSTEMMODAL + $MB_ICONERROR, "Error", "无法打开文件。")  
    EndIf
    Return True
EndFunc


;~ ------------------------------------------------------------
Func _GetTimeStr(byref $ts)
    Local $aData, $aTime
    _DateTimeSplit(_NowCalc(), $aData, $aTime)
    If @error Then
        MsgBox($MB_SYSTEMMODAL + $MB_ICONERROR, "Result", "_DateTimeSplit Error!!!")
    Else
        For $i = 1 To 3 Step 1
            If (StringLen($aData[$i]) = 1) Then
                $aData[$i] = "0" & $aData[$i]
            EndIf
            If (StringLen($aTime[$i]) = 1) Then
                $aTime[$i] = "0" & $aTime[$i]
            EndIf
        Next

        $ts = $aData[1] & $aData[2] & $aData[3] & "_" & $aTime[1] & $aTime[2] & $aTime[3] 
    EndIf
    Return True
EndFunc