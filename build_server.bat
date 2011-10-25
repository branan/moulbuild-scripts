call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
ECHO ON

cd C:\urulive\PlasmaDotNet\PlasmaCore
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaCore.csproj
cd ..\PlasmaNet
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaNet.csproj
cd ..\PlasmaServers
msbuild /property:Configuration=Release /property:Platform=x86 /t:Rebuild PlasmaServers.csproj