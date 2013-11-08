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
choice /c EA /M "Press E for Easy and A for Advanced."
if %errorlevel% ==1 set fromm=easy
if %errorlevel% ==2 set fromm=advanced
if %errorlevel% ==1 goto easy
if %errorlevel% ==2 goto filetype
cls
echo Error please try again.
pause
goto mainmenu


rem This displayes a simple menu for users to chose either advanced mode, Where you type the full path, or Easy mode, Where you 

type ony the folder name of a folder on the desktop.
rem This menu uses the choice command to make the user chose one of two choices.
rem After they chose it records which one the chose in fromm (from menu) so that they can be routed after they have thosen the 

file type.

:easy
set errorlevel=0
set fromm=easy
cls
echo The converted files will appear in the same folder with the ARF files in it.
set /p deskfolder=Enter the name of the folder on your desktop that contains the ARF file(s):
set source=%userprofile%\Desktop\%deskfolder%\
set dest=%source%
goto filetype


rem The user inputs the name of a folder on the desktop 
rem and it is combined with the system %userprofile% varible to 
rem make %source%. %source% is then copied into %dest% to set the destination of the MP4 files.


:filetype
cls
echo You have two file types to convert to: WMV and MP4.
echo WMV is the Windows Media Video format and is compatible with most computers and devices.
echo MP4 is MPEG Layer 4. It is compatible with almost all computers and devices.
rem SWF is a Shockwave Flash file. It is compatible with most web browsers with flash installed.
choice /c WM /m "Please chose which file you want to convert to: W=WMF, M=MP4"
if %errorlevel% EQU 1 set ftype=WMF
if %errorlevel% EQU 2 set ftype=MP4
if %errorlevel% EQU 3 set ftype=SWF
if fromm==easy goto where
if fromm==advanced goto source


rem The above gives you the choice to chose which formats that you can convert to. it does this by changing the %ftype% to the 

selected format then reading from which menu you came from (%fromm%, From Menu). After it has determined which one you came from 

it routs you to the approiate next step.



:source
set errorlevel=0
cls
echo Please select the folder with the ARF files in it.
set /p source=E.G. C:\Users\Elliot\Desktop\ARFs:
goto dest


rem This sets the folder location for the ARF files.


:dest
cls
echo Please select where the converted files should appear.
set /p dest=E.G. C:\Users\Elliot\Desktop\Converted:
goto where
cls
echo An error has occored.
echo Please email me with what happened.
echo elliot-labs@live.com
pause
goto end


rem This sets the output folder for the converted files.


:where
if %ftype% ==MP4 goto premp4cfg
if %ftype% ==WMV goto prewmvcfg
if %ftype% ==SWF goto preswfcfg
cls
echo An error has occored. Please email me with what happened :(
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
for %%a in ("%cd%\*.cfg") do c:\programdata\webex\webex\500\nbrplay.exe -Convert %%~a
del *.cfg
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it runs the NBRPLAY.exe -convert %%~a to process all of the config files in the %cd% folder then convert the specified 

ARF file (in the CFG file)


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


rem Above is the CFG file template used to apply to the ARF's CFG file.


:prewmvcfg
cls
echo Converting files... This may take some time so go get yourself a coffee and     watch your favorite TV show.
setlocal
set cd=%source%
cd /d %cd%
for %%a in ("%cd%\*.arf") do call:MakeWMVCFG "%%~a" "%dest%" "%source%"
for %%a in ("%cd%\*.cfg") do c:\programdata\webex\webex\500\nbrplay.exe -Convert %%~a
del *.cfg
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it runs the NBRPLAY.exe -convert %%~a to process all of the config files in the %cd% folder then convert the specified 

ARF file (in the CFG file)


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
ECHO([MP4]
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


rem Above is the CFG file template used to apply to the ARF's CFG file.


:preswfcfg
cls
echo You have somehow found thw SWF mode of the bulk converter. However the converter cannot convert to SWF at the moment. It 

will be here soon. Hang in there :-)
pause
goto end


rem The above is coming soon.


:nonbr
cls
echo You do not have WebEx's Network Recording Player installed.
echo Please go to http://www.webex.com/play-webex-recording.html
echo and download the ARF version
pause
goto end


rem The above is displayed if you do not have the Networking Recording Player (nbrplayer)
rem installed. It displays a link to the download page to the NBR tool.


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
pause | echo Press any key to exit...
exit /b


rem Exits the program on the user's input while giving the credits.
