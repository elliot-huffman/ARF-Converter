set filecount=0
for %%A in (*) do set /a filecount+=1
echo File count = %filecount%

rem Finds the number of files in the folder

:cfgname


goto createcfg

rem this sets the name of the CFG that will be created for the ARF file


:createcfg
echo [Console] >> %MP4%.cfg
echo inputfile=%source%\1.arf >> %MP4%.cfg
echo media=MP4 >> %MP4%.cfg
echo showui=1 >> %MP4%.cfg
echo [UI] >> %MP4%.cfg
echo chat=1 >> %MP4%.cfg
echo qa=0 >> %MP4%.cfg
echo largeroutline=1 >> %MP4%.cfg
echo [MP4] >> %MP4%.cfg
echo outputfile=%dest%\1.mp4 >> %MP4%.cfg
echo width=1024 >> %MP4%.cfg
echo height=768 >> %MP4%.cfg
echo framerate=10 >> %MP4%.cfg


rem This makes the config file that is required by the player to convert



set filecount=0
for %%A in (*) do set /a filecount+=1
echo File count = %filecount%
goto preloop


:preloop
set num=0
goto loop

:loop
cls
echo %num%
pause
set /a num+=1
if %num%==%filecount% (goto end) ELSE goto loop

