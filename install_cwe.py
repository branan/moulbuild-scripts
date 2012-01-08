#!/usr/bin/env python

import installer

files = [
"plClient.exe",
"plUruLauncher.exe",
"UruExplorer.exe",
"UruLauncher.exe",
"NxCharacter.dll",
"PhysXLoader.dll",
"python27.dll",
"PhysX_Setup.exe",
"oalinst.exe",
"Python/Python.pak",
"CREDITS.txt",
"LICENSE.txt"
]

installer.install("C:/urulive/gow/staging/", "data", files)