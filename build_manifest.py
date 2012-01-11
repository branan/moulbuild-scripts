#!/usr/bin/env python
import argparse
import os
import mfs

parser = argparse.ArgumentParser()
parser.add_argument("--data_root")
parser.add_argument("--srv_root")
parser.add_argument("--host")
parser.add_argument("--user")
args = parser.parse_args()

os.chdir(args.srv_root)

mfs.make_patcher_mfs(args.data_root)
mfs.make_client_mfs(args.data_root)
mfs.make_new_preloader_mfs(args.data_root, "31415926535897932384626433832795")
mfs.make_all_age_mfs(args.data_root)
os.rmdir(mfs.tmpdir)