@echo off
cd /d %~dp0

:setdir
set /p dir=Anaconda2��װλ�ã�D:\Path\To\Anaconda2����
if exist %dir%\Scripts\anaconda.exe (
    goto mklink
) else (
    echo ��Ч��·��
    pause
    goto setdir
)

:mklink
mklink /D Anaconda2 %dir%
pause
