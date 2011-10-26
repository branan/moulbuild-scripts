#!/usr/bin/env python

import argparse
import subprocess
import os

os.chdir("C:/urulive/staging")

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

parser = argparse.ArgumentParser()
parser.add_argument("--host")
parser.add_argument("--user")
parser.add_argument("--srv_root")

args = parser.parse_args()

remote_root = args.srv_root

copy_command = ""
if args.host == "localhost":
    copy_command = "cp"
else:
    copy_command = "scp"
    remote_root = ":".join(["@".join([args.user,args.host]), remote_root])

for f in files:
    local_file = ''.join(["./",f])
    remote_file = ''.join([remote_root,f])
    cmd = [copy_command, local_file, remote_file]
    process = subprocess.Popen(cmd)
    process.wait()
    if process.returncode != 0:
        raise RuntimeError()
