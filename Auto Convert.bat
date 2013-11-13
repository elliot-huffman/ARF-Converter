:start
@echo off
color 2e
cls
if not EXIST C:\programdata\webex\webex\500\nbrplay.exe goto nonbr
goto mainmenu


rem Set up the enviroment and color of this program.
rem Also checks if the required player is installed.


:mainmenu
cls
echo Easy mode: Enter the name of the folder on your desktop that contains your ARF  files.
echo Advanced mode: Enter the full path to the folder containing the ARF files.
echo.
choice /c EA /M "Press E for Easy and A for Advanced."
if %errorlevel%==1 set fromm=easy
if %errorlevel%==1 goto easy
if %errorlevel%==2 set fromm=advanced
if %errorlevel%==2 goto filetype
cls
echo There has been an error
echo Error Location "mainmenu"
pause
goto mainmenu


rem This displayes a simple menu for users to chose either advanced mode, Where you type 
rem the full path, or Easy mode, Where you type ony the folder name of a folder on the desktop.
rem
rem This menu uses the choice command to make the user chose one of two choices.
rem After they chose it records which one the chose in fromm (from menu) so that they can be routed after they have thosen the file type.


:easy
set fromm=easy
cls
echo The converted files will appear in the same folder with the ARF files in it.
echo.
echo Please enter, below, the name of the folder on your desktop that contains ARF files you wish to convert.
echo.
set /p deskfolder=Enter the folder name here:
set source=%userprofile%\Desktop\%deskfolder%\
set dest=%source%
goto filetype


rem The user inputs the name of a folder on the desktop 
rem and it is combined with the system %userprofile% varible to 
rem make %source%. %source% is then copied into %dest% to set the destination of the MP4 files.


:filetype
cls
echo You have two file types to convert to: WMV and MP4.
echo.
echo WMV is the Windows Media Video format and is compatible with most computers and devices.
echo.
echo MP4 is MPEG Layer 4. It is compatible with almost all computers and devices.
echo.
echo SWF is a Shockwave Flash file. It is compatible with most web browsers with flash installed. It is ideal for embedding in web pages.
echo.
echo.
set /p filetypechoice="Enter you chosen file type here. W=WMV M=MP4 S=SWF.  W, S or M?"
if %filetypechoice%==W set ftype=WMV
if %filetypechoice%==M set ftype=MP4
if %filetypechoice%==S set ftype=SWF
if %filetypechoice%==w set ftype=WMV
if %filetypechoice%==m set ftype=MP4
if %filetypechoice%==s set ftype=SWF
if %fromm%==easy goto where
if %fromm%==advanced goto source
cls
echo An error has occored. Please email me with the details.
echo Error Location "filetype"
echo elliot-labs@live.com
pause
goto end


rem The above gives you the choice to chose which formats that you can convert to. it does this by changing the %ftype% to the selected format then reading from which menu you 

came from (%fromm%, From Menu). After it has determined which one you came from it routs you to the approiate next step.



:source
cls
echo Make sure that you type the full path to the folder that contains the ARF files. I have not tested network shares. Yet...
echo.
echo Please select the folder with the ARF files in it.
set /p source=E.G. C:\Users\Elliot\Desktop\ARFs:
goto dest


rem This sets the folder location for the ARF files.


:dest
cls
echo Make sure that you type the full path to the folder that contains the ARF files. I have not tested network shares. Yet...
echo.
echo Please select where the converted files should appear.
set /p dest=E.G. C:\Users\Elliot\Desktop\Converted:
goto where
cls
echo An error has occored.
echo Please email me with what happened.
echo Error location "dest"
echo elliot-labs@live.com
pause
goto end


rem This sets the output folder for the converted files.


:where
if %ftype% EQU MP4 goto premp4cfg
if %ftype% EQU WMV goto prewmvcfg
if %ftype% EQU SWF goto preswfcfg
cls
echo An error has occored. Please email me with what happened :(
echo Error location "where"
echo elliot-labs@live.com
pause
goto end


rem The above code routes the user to the diffrent config makers based on there input.


:premp4cfg
cls
echo Converting files... This may take some time so go get yourself a coffee and     watch your favorite TV show.
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


rem Above is the CFG file template used to create the ARF's CFG file.


:prewmvcfg
cls
echo Converting files... This may take some time so go get yourself a coffee and     watch your favorite TV show.
setlocal
set cd=%source%
cd /d %cd%
for %%a in ("%cd%\*.arf") do call:MakeWMVCFG "%%~a" "%dest%" "%source%"
for %%a in ("%cd%\*.cfg") do set /a count +=1
for %%a in ("%cd%\*.cfg") do call:countnconvert "%%~a" "%source%" "%count%" & set /a count -=1
del *.cfg
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it calls the :countnconvert section and converts them while displaying the remaining file count.


:MakeWMVCFG
setlocal
set "WMV=%~n1"
set "source=%~dp1"
set "filename=%~n1"

(
ECHO([Console]
ECHO(inputfile="%source%\%filename%.arf"
ECHO(media=WMV
ECHO(showui=0
ECHO(PCAudio=0
ECHO([UI]
ECHO(chat=1
ECHO(video=0
ECHO(qa=0
ECHO(largeroutline=1
ECHO([WMV]
ECHO(outputfile="%dest%\%filename%.wmv"
ECHO(width=1440
ECHO(height=768
ECHO(videocodec=Windows Media Video 9
ECHO(audiocodec=Windows Media Audio 9.2 Lossless
ECHO(videoformat=default
ECHO(audioformat=default
ECHO(videokeyframes=4
ECHO(maxstream=1000
)>"%WMV%.cfg"
exit /b


rem Above is the CFG file template used to create the ARF's CFG file.


:preswfcfg
cls
setlocal
set count =0
set cd=%source%
cd /d %cd%
for %%a in ("%cd%\*.arf") do call:MakeSWFCFG "%%~a" "%dest%" "%source%"
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
ECHO(inputfile="%source%\%filename%.arf"
ECHO(media=SWF
ECHO(showui=0
ECHO(PCAudio=0
ECHO([SWF]
ECHO(outputfile="%dest%\%filename%.swf"
ECHO(width=1440
ECHO(height=768
)>"%SWF%.cfg"
exit /b


rem Above is the CFG file template used to create the ARF's CFG file.


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


:countnconvert
setlocal
cls
echo %count% files remaining... This may take some time ;)
c:\programdata\webex\webex\500\nbrplay.exe -Convert "%~dp1\%~n1.cfg"
exit /b


rem This converts the file based upon the inputed CFG file that was created in one of the previous steps.
rem This also displays the current files that are left for conversion.


:help
echo Coming soon...
pause
goto end


rem Coming soon... :)


:end
cls
echo Thank you for using the Elliot Labs ARF converter.
echo Special thanks to HuffDaddy for coding help.
echo For feature requests please email Elliot at elliot-labs@live.com
echo.
pause | echo Press any key to exit...
exit /b


rem Exits the program on the user's input while giving the credits.
