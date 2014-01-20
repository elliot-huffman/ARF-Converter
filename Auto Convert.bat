:start
@echo off
color 2e
cls
if not EXIST C:\programdata\webex\webex\500\nbrplay.exe goto nonbr
goto mainmenu


rem Also checks if the required program is installed.


:init


:mainmenu
cls
echo Easy mode: Enter the name of the folder on your desktop that contains your ARF  files.
echo Advanced mode: Enter the full path to the folder containing the ARF files.
echo Options: Configure the conversion process from frame rate to codecs
echo.
set /p mmenu=Press A for Advanced, E for Easy and O for Options. Then press enter:
if %mmenu%==1 set fromm=easy
if %mmenu%==1 goto easy
if %mmenu%==2 set fromm=advanced
if %mmenu%==2 goto filetype
if %mmenu%==3 set fromm=options
if %mmenu%==3 goto options
cls
echo There has been an error
echo Error Location "mainmenu"
pause
goto mainmenu


rem This displays a simple menu for users to chose either advanced mode, Where you type 
rem the full path, or Easy mode, Where you type ony the folder name of a folder on the desktop.
rem
rem This menu uses the choice command to make the user chose one of two choices.
rem After they chose it records which one the chose in %fromm% (from menu) so that they can be routed after they have chosen the file type.


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
rem and it is combined with the system %userprofile% variable to 
rem make %source%. %source% is then copied into %dest% to set the destination of the MP4 files.


:filetype
cls
echo You have three file types to convert to: WMV, SWF and MP4.
echo.
echo WMV is the Windows Media Video format and is compatible with most computers
echo.
echo MP4 is MPEG Layer 4. It is compatible with almost all computers and devices
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


:options
set omenu=4
cls
echo There are no SWF options avalable :(
echo.
echo Press 1 for global settings.
echo Press 2 for MP4 settings.
echo Press 3 for WMV settings.
echo Press 4 to go back to the Main Menu
echo.
set /p omenu=Press [1-4] then press enter:
if %omenu%==1 goto mGlobal
if %omenu%==2 goto mMP4
if %omenu%==3 goto mWMV
if %omenu%==4 goto mainmenu
cls
echo Something has went wrong. Please try again.
echo location: Options menu.
pause
goto options


:mWMV
set mWMV=4
cls
echo Press 1 for the "PCAudio" setting
echo Press 2 for Video Codec settings
echo Press 3 for Audio Codec settings
echo.
echo Press 4 to go back to the main options menu
echo.
echo.
set /p mWMV=Press [1-4] then press enter:
if %mWMV%==1 goto mPCAudio
if %mWMV%==2 goto videocodec
if %mWMV%==3 goto audiocodec 
if %mWMV%==4 goto options
cls
echo Something has went wrong. Please try again.
echo location: WMV options menu.
pause
goto mWMV


:mMP4
set mMP4=4
cls
echo These option effect only the MP4 file type.
echo.
echo for "Width" press 1
echo for "Height" press 2
echo for "Framerate" press 3
echo.
echo Press 4 to go back to the main options menu
echo.
echo.
set /p mMP4=Press [1-4] then press enter:
if %mMP4%==1 goto MP4Width
if %mMP4%==2 goto MP4Height
if %mMP4%==3 goto MP4Framerate
if %mMP4%==4 goto options
cls
echo Something has went wrong. Please try again.
echo location: mMP4.
pause
goto mMP4


:mGlobal
set mGlobal=6
cls
echo These options effect all file types.
echo.
echo Press 1 for the "ShowUI" setting
echo Press 2 for the "chat" setting
echo Press 3 for the "video" setting
echo Press 4 for the "largeroutline" setting
echo Press 5 for the "QA" setting
echo.
echo Press 6 to return to the main options menu
echo.
echo.
set /p mGlobal= Press [1-6] then press enter:
if %mGlobal%==1 goto mShowUI
if %mGlobal%==2 goto mChat
if %mGlobal%==3 goto mVideo
if %mGlobal%==4 goto mLargeoutline
if %mGlobal%==5 goto mQA
if %mGlobal%==6 goto options
cls
echo Something has went wrong. Please try again.
echo location: mGlobal.
pause
goto mGlobal


:mShowUI
cls
echo Press 1 to enable the showUI setting
echo Press 2 to Disable the showUI setting
set /p mshowUI=Press the desired number [1-2] then press enter:
if %mshowUI%==1 set showUI=1
if %mshowUI%==2 set showUI=0
cls
if %mshowUI%==1 echo ShowUI is enabled
if %mshowUI%==2 echo ShowUI is disabled
pause
goto mGlobal

:mQA
cls
echo Press 1 to show the QA box
echo Press 2 to hide the QA box
set /p mQA=Press the desired number [1-2] then press enter:
if %mQA%==1 set QA=1
if %mQA%==2 set QA=0
cls
if %mQA%==1 echo The QA box is enabled
if %mQA%==2 echo The QA box is disabled
pause
goto mGlobal


:mPCAudio
cls
echo Press 1 to enable the PCAudio setting
echo Press 2 to Disable the PCAudio setting
set /p mPCAudio=Press the desired number [1-2] then press enter:
if %mPCAudio%==1 set PCAudio=1
if %mPCAudio%==2 set PCAudio=0
cls
if %mPCAudio%==1 echo PCAudio is enabled
if %mPCAudio%==2 echo PCAudio is disabled
pause
goto mWMV


:MP4Width
cls
echo Please enter a witdth resolution (in pixles).
echo.
set /p MP4Width=Enter desired width for resolution here:
cls
echo You have set %MP4Width% as the desired width.
pause
goto mMP4


:MP4Height
cls
echo Please enter a height resolution (in pixles).
echo.
set /p MP4Height=Enter the desired height for resolution here:
cls
echo You have set %MP4Height% as the desired height.
pause
goto mMP4


:MP4Framerate
cls 
echo Please enter a desired frame rate (in frames per second).
echo.
echo The optimal framerates are 3 for low quality, 5 for medium and
echo 8 for high. although you can use frame rates higher then the above
echo you might not get better results.
echo.
set /p MP4Framerate=Enter the desired frame rate here then press enter:
cls
echo You have set %MP4Framerate% as the desired frame rate.
if %MP4Framerate%==0 echo This is an incorrect frame rate. Please enter a valid frame rate.
pause
if %MP4Framerate%==0 goto MP4Framerate
goto mMP4


:mChat
cls
echo Press 1 to display the Chat window
echo Press 2 to hide the chat window
set /p mChat=Press the desired number [1-2] then press enter:
if %mChat%==1 set Chat=1 
if %mChat%==2 set Chat=0
cls
if %mChat%==1 echo You have enabled the chat window.
if %mChat%==2 echo You have disabled the chat window.
pause
goto mGlobal


:mVideo
cls
echo Press 1 to display the Video window
echo Press 2 to hide the Video window
set /p mVideo=Press the desired number [1-2] then press enter:
if %mVideo%==1 set Video=1 
if %mVideo%==2 set Video=0
cls
if %mVideo%==1 echo You have enabled the video window.
if %mVideo%==2 echo You have disabled the video window.
pause
goto mGlobal


:mLargeoutline
cls
echo Press 1 to enable the Largeoutline setting
echo Press 2 to Disable the Largeoutline setting
set /p mLargeoutline=Press the desired number [1-2] then press enter:
if %mLargeoutline%==1 set Largeoutline=1
if %mLargeoutline%==2 set Largeoutline=0
cls
if %mLargeoutline%==1 echo You have enabled Largeoutline.
if %mLargeoutline%==2 echo You have disabled Largeoutline.
pause
goto mGlobal


:videocodec
cls
echo Press 1 for: Windows Media Video 9
echo Press 2 for: Windows Media Video 9 Screen
echo.
set /p mvcodec=Press [1 or 2] then press enter:
if %mvcodec%==1 set vcodec=Windows Media Video 9
if %mvcodec%==2 set vcodec=Windows Media Video 9 Screen
cls
echo You have set the Video codec to:
echo %vcodec%
pause
goto mWMV


:audiocodec
cls 
echo Press 1 for: Windows Media Audio 9.2
echo Press 2 for: Windows Media Audio 9.2 Lossless
echo Press 3 for: Windows Media Audio 10 Professional
echo.
set /p macodec=Press [1-3] then press enter:
if %macodec%==1 set acodec=Windows Media Audio 9.2
if %macodec%==2 set acodec=Windows Media Audio 9.2 Lossless
if %macodec%==3 set acodec=Windows Media Audio 10 Professional
cls
echo You have set the Audio codec to:
echo %acodec%
pause
goto mWMV


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


rem This converts the file based upon the imputed CFG file that was created in one of the previous steps.
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
