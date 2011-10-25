call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
ECHO ON

cd C:\urulive\build\Plasma_int
jom -j4 plClient MaxMain MaxPlasmaLights plPythonPack
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\plClient.exe ..\..\staging\plClient.exe
copy /y bin\PlasmaMax.gup ..\..\staging\plugins\PlasmaMax.gup
copy /y bin\MaxPlasmaLights.dlo ..\..\staging\plugins\MaxPlasmaLights.dlo
copy /y bin\plPythonPack.exe ..\..\prefix\bin\plPythonPack.exe

cd C:\urulive\build\Plasma_ext
jom -j4 plClient plUruLauncher
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\UruExplorer.exe ..\..\staging\UruExplorer.exe
copy /y bin\UruLauncher.exe ..\..\staging\UruLauncher.exe

exit 0

:BUILDFAIL
exit 1