:start
@echo off
color 2e
cls
cd /d %~dp0
if not EXIST C:\programdata\webex\webex\500\nbrplay.exe goto nonbr
goto precfg

rem Checks if the required program is installed, turns off the output of commands and sets the color of the terminial. After it has completed the above tasks it routs the user to the main menu

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

rem The above is displayed if you do not have the Networking Recording Player (nbrplayer)
rem installed. It displays a link to the download page to the NBR tool.

:precfg
cls
setlocal
for %%a in ("%cd%\*.arf") do call:MakeSWFCFG "%%~a" "%source%\Converted" "%source%"
for %%a in ("%cd%\*.cfg") do set /a count +=1
for %%a in ("%cd%\*.cfg") do call:countnconvert "%%~a" "%source%" "%count%" & set /a count -=1
del *.cfg
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it calls the :countnconvert section and converts them while displaying the remaining file count.


:MakeSWFCFG
setlocal
set "SWF=%~n1"
set "source=%~dp1"
set "filename=%~n1"

(
ECHO([Console]
ECHO(inputfile="%source%%filename%.arf"
ECHO(media=SWF
ECHO(showui=0
ECHO(PCAudio=0
ECHO([SWF]
ECHO(outputfile="%source%Converted\%filename%.swf"
ECHO(width=1440
ECHO(height=768
)>"%SWF%.cfg"
exit /b


rem Above is the CFG file template used to create the ARF's CFG file.

:countnconvert
setlocal
cls
echo %count% files remaining... This may take some time ;)
c:\programdata\webex\webex\500\nbrplay.exe -Convert "%~dp1\%~n1.cfg"
exit /b

rem This converts the file based upon the imputed CFG file that was created in one of the previous steps.
rem This also displays the current files that are left for conversion.

:end
cls
echo Thank you for using the Elliot Labs ARF converter.
echo Special thanks to HuffDaddy for coding help.
echo For feature requests please email Elliot at elliot-labs@live.com
echo.
pause | echo Press any key to exit...
exit /b

rem Exits the program on the user's input while giving the credits.
