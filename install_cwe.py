#!/usr/bin/env python

import installer

files = [
"plClient.exe",
"plUruLauncher.exe",
"plCrashHandler.exe",
"UruExplorer.exe",
"UruLauncher.exe",
"UruCrashHandler.exe",
"NxCharacter.dll",
"PhysXLoader.dll",
"python27.dll",
"PhysX_Setup.exe",
"Python/Python.pak",
"CREDITS.txt",
"LICENSE.txt"
]

installer.install("C:/urulive/gow/staging/", "data", files)