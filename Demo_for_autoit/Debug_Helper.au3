#include <File.au3>
#include <FileConstants.au3>
#include <WinAPIFiles.au3>

#include <Date.au3>

#include <AutoItConstants.au3>

#include <MsgBoxConstants.au3>

; Press Esc to terminate script,

;~ crtl  : ^
;~ shift : +
;~ alt   : !

HotKeySet("{ESC}", "_Terminate")  ; esc
HotKeySet("^1", "_AutoStep")      ; ctrl + 1

Dim $wd = @ScriptDir

Dim $hWnd = WinGetHandle("[CLASS:Chrome_WidgetWin_1]", "")

Dim $time_str = ""
_GetTimeStr($time_str)


Dim $fn = "Log_ff_"
Dim $fp_s = $wd & "\" & $fn & $time_str & "_s.txt"
Dim $fp_f = $wd & "\" & $fn & $time_str & "_f.txt"

Dim $src_path = "xxxxxx"

Dim $init_info = "NullInfo"
Dim $last_path_info = ""
Dim $curr_path_info = ""
Dim $line_info = ""

Dim $prog_succeed = False


Dim $loop_n = 10000


Dim $arr_s[$loop_n]
Dim $arr_f[$loop_n]



;~ ------------------------------------------------------------
_PrepareLogFile($fp_s)
_PrepareLogFile($fp_f)
_InitArr()

;~ ------------------------------------------------------------
;~ main loop to waite hotkey press
MsgBox($MB_SYSTEMMODAL, "AutoIt", "Prog Start.", 0.5)
While 1
    Sleep(100)
WEnd





;~ ------------------------------------------------------------
Func _Terminate()
    If Not $prog_succeed Then
        _ArrAppend2Txt($fp_s, $arr_s)
        _ArrAppend2Txt($fp_f, $arr_f)
    EndIf

    _StrAppend2Txt($fp_s, ">>> End Recording: ")
    _StrAppend2Txt($fp_f, ">>> End Recording: ")

    MsgBox($MB_SYSTEMMODAL, "AutoIt", "Script Terminate!!.")
    ;~ Prog Exit Here
    Exit
EndFunc


Func _InitArr()
    For $i = 0 To UBound($arr_s) - 1
        $arr_s[$i] = ""
        $arr_f[$i] = ""
    Next
    Return True
EndFunc

Func _OneStepForward()
    Sleep(25)
    Send("{F11}")
    Return True
EndFunc

Func _OneStepBackward()
    Sleep(25)
    Send("+{F11}")
    Return True
EndFunc

Func _GetFilePathInfo()
    ;~ clear the clipboard before inject info
    Sleep(100)
    ClipPut($init_info)
    $curr_path_info = $init_info

    Do
        ;~ vscode hotkeys to get the current file path
        Send("+!c")
        Sleep(50)
    
        ;~ get from clipboard
        $curr_path_info = ClipGet()
    Until StringCompare($curr_path_info, $init_info) <> 0
EndFunc


Func _GetLineInfo()
    ;~ clear the clipboard before inject info
    Sleep(100)
    ClipPut($init_info)
    $line_info = $init_info

    Do
        ;~ vscode hotkeys to get the current file path
        Send("+!c")
        Sleep(50)
    
        ;~ get from clipboard
        $line_info = ClipGet()
    Until StringCompare($line_info, $init_info) <> 0
EndFunc


;~ ------------------------------------------------------------
Func _AutoStep()
    $prog_succeed = False
    _InitArr()

    For $i = 0 To UBound($arr_s) - 1
        ;~ focus to vscode
        If (Not WinActive($hWnd)) Then
            WinActivate($hWnd)
        EndIf

        _OneStepForward()
        _GetFilePathInfo()
        
        While (Not StringInStr($curr_path_info, $src_path)) or StringInStr($curr_path_info, "psfw_")
            _OneStepBackward()
            _GetFilePathInfo()
        WEnd


        ;~ compare before take record
        If ($last_path_info <> $curr_path_info) Then
            ;~ take record
            $last_path_info = $curr_path_info
            ;~ add timp stamp & inject to array
            $arr_s[$i] = _NowCalc() & " | " & $curr_path_info
        EndIf
        _GetLineInfo()
        $arr_f[$i] = _NowCalc() & " | " & $curr_path_info  & " | " & $line_info 
    Next

    ;~ write to file
    _ArrAppend2Txt($fp_s, $arr_s)
    _ArrAppend2Txt($fp_f, $arr_f)

    ;~ show some popup box, 
    ;~ what's more important is that: after box shown, focus will jump out of vscode & waitfor autoit
    MsgBox($MB_SYSTEMMODAL, "AutoIt", "Path Copy.", 0.5)

    ;~ focus handback to vscode
    If (Not WinActive($hWnd)) Then
        WinActivate($hWnd)
    EndIf

    $prog_succeed = True

EndFunc






;~ ------------------------------------------------------------
Func _PrepareLogFile($fp)
    If FileExists($fp) Then
        FileDelete($fp)
    EndIf
    $file = FileOpen($fp, $FO_CREATEPATH + $FO_OVERWRITE)
    FileWriteLine($file, ">>> Start Recording: ") 
    FileClose($file) 
    Return True
EndFunc


;~ ------------------------------------------------------------
Func _StrAppend2Txt($fp, $curr_path_info)
    $file = FileOpen($fp, $FO_APPEND)
    If $file <> -1 Then
        FileWriteLine($file, $curr_path_info)  
        FileClose($file)  
    Else  
        MsgBox($MB_SYSTEMMODAL + $MB_ICONERROR, "Error", "无法打开文件。")  
    EndIf
    Return True
EndFunc



;~ ------------------------------------------------------------
Func _ArrAppend2Txt($fp_s, $arr)
    $file = FileOpen($fp_s, $FO_APPEND)
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

