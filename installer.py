import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("--host")
parser.add_argument("--user")
parser.add_argument("--srv_root")
parser.add_argument("--data_root")

args = parser.parse_args()

remote_roots = {}

copy_command = ""
if args.host == "localhost":
    copy_command = "cp"
    remote_roots["data"] = args.data_root
    remote_roots["srv"] = args.srv_root
else:
    copy_command = "scp"
    remote_roots["data"] = ":".join(["@".join([args.user,args.host]), args.data_root])
    remote_roots["srv"] = ":".join(["@".join([args.user,args.host]), args.srv_root])

def install(source_path, remote_root, files):
    os.chdir(source_path)
    for f in files:
        local_file = ''.join(["./",f])
        remote_file = ''.join([remote_roots[remote_root],f])
        cmd = [copy_command, local_file, remote_file]
        process = subprocess.Popen(cmd)
        process.wait()
        if process.returncode != 0:
            raise RuntimeError()