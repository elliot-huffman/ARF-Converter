:start
@echo off
cls
cd /d %~dp0
goto preloop

:preloop
set num=0
goto loop

:loop
cls
echo %num%
pause
set /a num+=1
if %num%==6 (goto end) ELSE goto loop





:end
cls
echo Works!
pause
