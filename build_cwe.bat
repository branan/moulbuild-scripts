call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
ECHO ON

cd C:\urulive\gow\Plasma
call git pull
IF ERRORLEVEL 1 GOTO BUILDFAIL

cd C:\urulive\gow\build_int
jom clean
jom -j6 plClient plUruLauncher
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\plClient.exe ..\staging\plClient.exe
copy /y bin\plUruLauncher.exe ..\staging\plUruLauncher.exe


cd C:\urulive\gow\build_ext
jom clean
jom -j6 plClient plUruLauncher
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\UruExplorer.exe ..\staging\UruExplorer.exe
copy /y bin\UruLauncher.exe ..\staging\UruLauncher.exe


exit 0

:BUILDFAIL
exit 1