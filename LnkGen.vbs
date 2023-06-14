
pyFN = "\Demo_for_dot\md2dot2png.py"
exeFN = "%userprofile%\.conda\envs\MyEnv\pythonw.exe"
lnkFN = "\md2dot2png.lnk"

set WshShell = CreateObject("WScript.Shell")

strDesktop = WshShell.SpecialFolders("Desktop")
currentPath = WshShell.CurrentDirectory
REM msgbox currentPath
set oMyShortCut = WshShell.CreateShortcut(strDesktop + lnkFN)

REM exePath = currentPath + exeFN
exePath = exeFN
pyPath = chr(34) + currentPath + pyFN + chr(34)

oMyShortCut.WindowStyle = 1
oMyShortcut.IconLocation = exePath
oMyShortCut.TargetPath = exePath
oMyShortCut.Arguments = pyPath
oMyShortCut.WorkingDirectory = currentPath
oMyShortCut.Save

