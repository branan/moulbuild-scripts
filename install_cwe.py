#!/usr/bin/env python

import installer

files = [
"plClient.exe",
"plClient.pdb",
"UruExplorer.exe",
"UruExplorer.pdb",
"UruLauncher.exe",
"NxCharacter.dll",
"NxCooking.dll",
"PhysXLoader.dll",
"python27.dll",
"PhysX_Setup.exe",
"oalinst.exe",
"python/python.pak",
"CREDITS.txt",
"LICENSE.txt"
]

installer.install("C:/urulive/staging/", "data", files)