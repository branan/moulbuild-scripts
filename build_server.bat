call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
ECHO ON

cd C:\urulive\PlasmaDotNet
call git pull origin master
IF ERRORLEVEL 1 GOTO BUILDFAIL

cd PlasmaCore
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaCore.csproj
IF ERRORLEVEL 1 GOTO BUILDFAIL

cd ..\PlasmaNet
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaNet.csproj
IF ERRORLEVEL 1 GOTO BUILDFAIL

cd ..\PlasmaServers
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaServers.csproj
IF ERRORLEVEL 1 GOTO BUILDFAIL

exit 0

:BUILDFAIL
echo "skipped to buildfail"
exit 1