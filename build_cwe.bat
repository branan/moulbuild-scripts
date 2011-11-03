call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
ECHO ON

cd C:\urulive\Plasma
git pull

cd C:\urulive\build\Plasma_max12
jom clean
jom -j6 MaxMain MaxPlasmaLights
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\PlasmaMax.gup ..\..\staging\plugin2012\PlasmaMax.gup
copy /y bin\MaxPlasmaLights.dlo ..\..\staging\plugin2012\MaxPlasmaLights.dlo

cd C:\urulive\build\Plasma_max10
jom clean
jom -j6 MaxMain MaxPlasmaLights
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\PlasmaMax.gup ..\..\staging\plugin2010\PlasmaMax.gup
copy /y bin\MaxPlasmaLights.dlo ..\..\staging\plugin2010\MaxPlasmaLights.dlo

cd C:\urulive\build\Plasma_int
jom clean
jom -j6 plClient plPythonPack MaxMain MaxPlasmaLights
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\plClient.exe ..\..\staging\plClient.exe
copy /y bin\plClient.pdb ..\..\staging\plClient.pdb
copy /y bin\PlasmaMax.gup ..\..\staging\plugin2011\PlasmaMax.gup
copy /y bin\MaxPlasmaLights.dlo ..\..\staging\plugin2011\MaxPlasmaLights.dlo
copy /y bin\plPythonPack.exe ..\..\prefix\bin\plPythonPack.exe

cd C:\urulive\build\Plasma_ext
jom clean
jom -j6 plClient plUruLauncher
IF ERRORLEVEL 1 GOTO BUILDFAIL
copy /y bin\UruExplorer.exe ..\..\staging\UruExplorer.exe
copy /y bin\UruExplorer.pdb ..\..\staging\UruExplorer.pdb
copy /y bin\UruLauncher.exe ..\..\staging\UruLauncher.exe

exit 0

:BUILDFAIL
exit 1