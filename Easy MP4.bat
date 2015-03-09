:start
@echo off
color 2e
cls
cd /d %~dp0
if not EXIST C:\programdata\webex\webex\500\nbrplay.exe goto nonbr

:nonbr
cls
echo You do not have WebEx's Network Recording Player installed.
echo.
echo Pressing "Y" will open http://www.webex.com/play-webex-recording.html
echo Pressing "N" will jump the program to the end.
echo.
choice /m "NOTE: When you download the player, download the ARF version."
if %errorlevel% EQU 2 goto end
cls
echo I have opened the above link in you web browser.
echo.
echo NOTE: Download and install the ARF version!!!
start www.webex.com/play-webex-recording.html
pause
goto end

:precfg
cls
setlocal
set cd=%source%
cd /d %cd%
for %%a in ("%cd%\*.arf") do call:MakeMP4CFG "%%~a" "%dest%" "%source%"
for %%a in ("%cd%\*.cfg") do set /a count +=1
for %%a in ("%cd%\*.cfg") do call:countnconvert "%%~a" "%source%" "%count%" & set /a count -=1
del *.cfg
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it calls the :countnconvert section and converts them while displaying the remaining file count.


:MakeMP4CFG
setlocal
set "MP4=%~n1"
set "source=%~dp1"
set "filename=%~n1"

(
ECHO([Console]
ECHO(inputfile="%source%\%filename%.arf"
ECHO(media=MP4
ECHO(showui=0
ECHO([UI]
ECHO(chat=1
ECHO(video=0
ECHO(qa=0
ECHO(largeroutline=1
ECHO([MP4]
ECHO(outputfile="%dest%\%filename%.mp4"
ECHO(width=1440
ECHO(height=768
ECHO(framerate=10
)>"%MP4%.cfg"
exit /b

:countnconvert
setlocal
cls
echo %count% files remaining... This may take some time ;)
c:\programdata\webex\webex\500\nbrplay.exe -Convert "%~dp1\%~n1.cfg"
exit /b
