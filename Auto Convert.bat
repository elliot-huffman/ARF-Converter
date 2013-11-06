@echo off
echo Please select the folder with the ARF files in it.
set /p source=E.G. C:\Users\Elliot\Desktop\HAOH:

rem This sets the folder location for the ARF files.
rem I am going to add a menu for simplicity sake later.


echo Please select where the mp4 files should appear.
set /p dest=E.G. C:\Users\Elliot\Desktop\Converted:


rem This sets the output folder for the converted files.
rem Again I will make a menu in the future.


setlocal
set cd=%source%
cd %cd%
for %%a in ("%cd%\*.arf") do call:MakeCFG "%%~a" "%dest%" "%source%"
for %%a in ("%cd%\*.cfg") do c:\programdata\webex\webex\500\nbrplay.exe -Convert %%~a
goto end


rem lists the contents of %cd% and puts the list in %%a.
rem Then processes the list (%a) and runs the call command for each entry while passing
rem the preselected destination and source to the config file that is created.

rem After that is done it then looks and makes a list of all the config files in the %cd% folder, again as %a.
rem Then it runs the NBRPLAY.exe -convert %%~a to process all of the config files in the %cd% folder then convert the specified ARF file (in the CFG file)


:MakeCFG
setlocal
set "MP4=%~n1"
set "source=%~dp1"
set "filename=%~n1"

(
ECHO([Console]
ECHO(inputfile=%source%%filename%.arf
ECHO(media=MP4
ECHO(showui=1
ECHO([UI]
ECHO(chat=1
ECHO(qa=0
ECHO(largeroutline=1
ECHO([MP4]
ECHO(outputfile=%dest%\%filename%.mp4
ECHO(width=1024
ECHO(height=768
ECHO(framerate=10
)>"%MP4%.cfg"
exit /b

rem Above is the CFG file template used to apply to the ARF's CFG file.



:end
cls
echo Thank you for using the Elliot Labs ARF converter.
echo Special thanks to HuffDaddy for coding help.
echo For feature requests please email Elliot at elliot-labs@live.com
pause | echo Press any key to exit...
exit /b

rem Exits the program on the user's input while giving the credits.
