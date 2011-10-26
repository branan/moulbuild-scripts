#!/usr/bin/env python

import installer

files = [
"plClient.exe",
"UruExplorer.exe",
"UruLauncher.exe",
"NxCharacter.dll",
"NxCooking.dll",
"OpenAL32.dll",
"PhysXLoader.dll",
"python27.dll",
"PhysX_Setup.exe",
"python/python.pak"
]

installer.install("C:/urulive/staging/", "data", files)