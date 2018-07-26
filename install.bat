@echo off
cd /d %~dp0

:setdir
set /p dir=Anaconda2安装位置（D:\Path\To\Anaconda2）：
if exist %dir%\Scripts\anaconda.exe (
    goto mklink
) else (
    echo 无效的路径
    pause
    goto setdir
)

:mklink
mklink /D Anaconda2 %dir%
pause
