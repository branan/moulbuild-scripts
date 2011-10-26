cd C:\urulive\moul-scripts\python
plPythonPack
IF ERRORLEVEL 1 GOTO BUILDFAIL

copy /y python.pak ..\..\staging\python\python.pak

exit 0

:BUILDFAIL
exit 1