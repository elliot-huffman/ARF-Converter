:start
@echo off
cls
cd /d %~dp0
goto source

rem This sets up the working folder. I usually do this because I need to but I am 
rem not sure about it this time...

:source
echo Please select the folder with the ARF files in it.
set /p source=E.G. C:\Users\Elliot\Desktop\toconvert:
goto dest


rem This sets the folder location for the ARF files.
rem I am going to add a menu for simplicity sake later.


:dest
echo Please select where the mp4 files should appear.
set /p dest=E.G. C:\Users\Elliot\Desktop\Converted:
goto cfgname


rem This sets the output folder for the converted files.
rem Again I will make a menu in the future.


:cfgname


goto createcfg

rem this sets the name of the CFG that will be created for the ARF file


:createcfg
echo [Console] >> %MP4%.cfg
echo inputfile=%source%\1.arf >> MP4.cfg
echo media=MP4 >> MP4.cfg
echo showui=1 >> MP4.cfg
echo [UI] >> MP4.cfg
echo chat=1 >> MP4.cfg
echo qa=0 >> MP4.cfg
echo largeroutline=1 >> MP4.cfg
echo [MP4] >> MP4.cfg
echo outputfile=%dest%\1.mp4 >> MP4.cfg
echo width=1024 >> MP4.cfg
echo height=768 >> MP4.cfg
echo framerate=10 >> MP4.cfg


rem This makes the config file that is required by the player to convert

:convert
cd C:\programdata\webex\webex\500
nbrplay.exe -Convert "%cfg%"

:end
echo Thanks for using Elliot Labs Auto Converter.
echo for feature requests please email: elliot-labs@live.com
pause | echo Press any key to exit...
exit

:preloop
set num=0
goto loop

:loop
cls
echo %num%
pause
set /a num+=1
if %num%==6 (goto end) ELSE goto loop
