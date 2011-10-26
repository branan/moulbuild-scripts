#!/usr/bin/env python

import installer

files = [
"ICSharpCode.SharpZipLib.dll",
"PlasmaCore.dll",
"PlasmaNet.dll",
"PlasmaServers.exe",
]

installer.install("C:/urulive/PlasmaDotNet/PlasmaServers/bin/Release", "srv", files)
