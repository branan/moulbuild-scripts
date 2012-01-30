#!/usr/bin/env python
from __future__ import print_function
from hashlib import md5
from optparse import OptionParser # argparse sucks.
from PyHSPlasma import *
import gzip
import os, os.path
import tempfile
import shutil

done = {}
class ProcessedFile:
    hash_un = None
    hash_gz = None
    size_un = 0
    size_gz = 0
    

# The manifest flags
# No, you're not insane!
# These are the same ones from UU...
kNone             = 0x00
kDualChannelOgg   = 0x01
kStreamOgg        = 0x02
kStereoOgg        = 0x04
#kGZip             = 0x08 <--- EVERYTHING is gzipped in MOUL
# End flags

tmpdir = tempfile.mkdtemp()

parser = OptionParser()
parser.add_option("-a", "--age", dest="age",
                  help="AGE we should generate manifests for", metavar="AGE",
                  default="External")
parser.add_option("-d", "--droid", dest="droid",
                  help="DROID key to use for SecurePreloader lists", metavar="DROID",
                  default="31415926535897932384626433832795")
parser.add_option("-c", "--complete", dest="complete",
                  help="Should we generate a COMPELTE file server's worth of manifests?", metavar="COMPLETE",
                  action="store_true", default=False)
parser.add_option("-s", "--source", dest="source",
                  help="MOUL install to use as a SOURCE", metavar="SOURCE",
                  default="G:\\Plasma\\Games\\Writers Shard")


def create_manifest(name):
    if not os.path.exists("FileSrv"):
        os.mkdir("FileSrv")
    
    file = open(os.path.join("FileSrv", name + ".mfs"), "w+")
    return file


# The magical turdfest?
def do_file(file, src, subfolder = None, flag = kNone, encrypt=False):
    global done
    
    if subfolder:
        gzpath = os.path.join(subfolder, file + ".gz")
    else:
        gzpath = file + ".gz"
    
    if file in done:
        # Haaaax
        f = done[file]
    else:
        # First, let's go ahead and prep the things and stuff
        realpath = os.path.join(src, file)
        if subfolder:
            endpath = os.path.join("FileSrv", os.path.join(subfolder, file + ".gz"))
        else:
            endpath = os.path.join("FileSrv", file + ".gz")
        
        tomake = os.path.split(endpath)[0]
        if not os.path.exists(tomake):
            os.makedirs(tomake) # Make all the dirs we need
        
        # Sanity check...
        if not os.path.isfile(realpath):
            plDebug.Error("FUCK! Can't find: %s" % realpath)
            return ""

        if encrypt:
            fname = os.path.basename(file)
            tmppath = os.path.join(tmpdir, fname)
            handle = open(realpath, "rb")
            data = handle.read()
            handle.close()
            stream = plEncryptedStream()
            stream.open(tmppath, fmCreate, plEncryptedStream.kEncXtea)
            stream.write(data)
            stream.close()
            readpath = tmppath
        else:
            readpath = realpath
            
        
        # MD5 the file
        f = ProcessedFile()
        handle = open(readpath, "rb")
        content = handle.read()
        f.hash_un = md5(content).hexdigest()
        handle.close()
        
        # Python rocks
        gz = gzip.open(endpath, mode='w+b')
        gz.write(content)
        gz.close()
        
        # Now we must waste some time...
        # This is all because eric sucks.
        handle = open(endpath, "rb")
        f.hash_gz = md5(handle.read()).hexdigest()
        handle.close()

        # cleanup the tmp file if we encrypted
        if encrypt:
            os.unlink(tmppath)
        
        #Grab some final info
        stat    = os.stat(realpath)
        stat_gz = os.stat(endpath)
        
        # Continue saving...
        f.size_un = stat.st_size
        f.size_gz = stat_gz.st_size
        done[file] = f
    
    line = "%s,%s,%s,%s,%s,%s,%s" % (file.replace("/", "\\"), gzpath, f.hash_un, f.hash_gz, f.size_un, f.size_gz, flag)
    print(line) # Debugging or just awesome output? You decide!
    return line + "\n"


def make_age_mfs(age, src):    
    mfs = create_manifest(age)
    mfs.write(do_file(os.path.join("dat", age + ".age"), src, encrypt=True))
    
    # Do FNI and CSV Manually
    # This is because Cyan sucks
    fni = os.path.join("dat", age + ".fni")
    if os.path.exists(fni):
        mfs.write(do_file(fni, src, encrypt=True))
    csv = os.path.join("dat", age + ".csv")
    if os.path.exists(csv):
        mfs.write(do_file(csv, src, encrypt=True))
    
    # Use the plResManager to find the pages
    # and figure out the sfx flags
    res = plResManager()
    agepath = os.path.join(os.path.join(src, "dat"), age + ".age")
    info = res.ReadAge(agepath, True)
    ver = res.getVer()
    
    # Grab the pages
    for i in range(info.getNumCommonPages(ver)):
        prp = info.getCommonPageFilename(i, ver)
        mfs.write(do_file(os.path.join("dat", prp), src))
    
    for i in range(info.getNumPages()):
        prp = info.getPageFilename(i, ver)
        mfs.write(do_file(os.path.join("dat", prp), src))
    
    # Now, we do the fun part and enumerate the sfx
    for loc in res.getLocations():
        for key in res.getKeys(loc, plFactory.ClassIndex("plSoundBuffer")):
            sbuf = key.object # Lazy
            
            flags = kNone
            if (sbuf.flags & plSoundBuffer.kOnlyLeftChannel) or (sbuf.flags & plSoundBuffer.kOnlyRightChannel):
                flags |= kDualChannelOgg
            else:
                flags |= kStereoOgg
            
            #Do we need to decompress this into a WAV file?
            if sbuf.flags & plSoundBuffer.kStreamCompressed:
                flags |= kStreamOgg
            
            #Go, go go!
            mfs.write(do_file(os.path.join("sfx", sbuf.fileName), src, flag=flags))
    
    # Explicitly kill off the resmgr because I feel like it
    del res
 
 
def make_all_age_mfs(src):
    dir = os.listdir(os.path.join(src, "dat"))
    for entry in dir:
        # We only want .age files
        if entry[len(entry) - 4:].lower() != ".age":
            continue
        
        make_age_mfs(entry[:len(entry) - 4], src)   


def make_client_mfs(src):
    internal = create_manifest("Internal")
    external = create_manifest("External")
    dir = os.listdir(src)
    
    # Check out the root directory and see what we have
    gotExt = False
    gotInt = False
    for entry in dir:
        path = os.path.join(src, entry)
        
        #If it's not a file, then we obviously don't want it
        if not os.path.isfile(path):
            continue
        # We don't want shortcuts (read: hacks)
        if entry[len(entry) - 4:].lower() == ".lnk":
            continue
        # We also don't want the patcher
        if entry.lower() == "urulauncher.exe" or entry.lower() == "plurulauncher.exe":
            continue
        # No server.ini
        if entry[len(entry) - 4:].lower() == ".ini":
            continue
        
        # Alrighty, we passed the checks, so
        # let's make a line!
        line = do_file(entry, src, "Client")
        
        # Make sure internal stuff gets in the internal manifest
        # and external stuff in the external manifest
        if entry.lower() == "plclient.exe":
            internal.write(line)
            gotInt = True
        elif entry.lower() == "uruexplorer.exe":
            external.write(line)
            gotExt = True
        else:
            internal.write(line)
            external.write(line)
    
    # Let's repeat the process for avi
    avi = os.path.join(src, "avi")
    dir = os.listdir(avi)
    for entry in dir:
        path = os.path.join(avi, entry)
        rel = os.path.relpath(path, src)
        ext = entry[len(entry) - 4:].lower()
        
        #If it's not a file, then we obviously don't want it
        if not os.path.isfile(path):
            continue
        # If it's not an AVI, bik, ogg, or ogv, goodbye!
        if not (ext == ".avi" or ext == ".bik" or ext == ".ogg" or ext == ".ogv"):
            continue
        
        line = do_file(rel, src)
        internal.write(line)
        external.write(line)

    # Let's repeat the process for the age files
    avi = os.path.join(src, "dat")
    dir = os.listdir(avi)
    for entry in dir:
        path = os.path.join(avi, entry)
        rel = os.path.relpath(path, src)
        ext = entry[len(entry) - 4:].lower()
        
        #If it's not a file, then we obviously don't want it
        if not os.path.isfile(path):
            continue
        # If it's not an age or a font, goodbye!
        if ext == ".age":
            line = do_file(rel, src, encrypt=True)
        elif ext == ".p2f"  or ext == ".loc":
            line = do_file(rel, src)
        else:
            continue
        
        internal.write(line)
        external.write(line)
    
    # Done with the main manifests, so let's close them
    internal.close()
    external.close()
    
    # Delete garbage (hack)
    if not gotExt:
        os.unlink(os.path.join("FileSrv", "External.mfs"))
    if not gotInt:
        os.unlink(os.path.join("FileSrv", "Internal.mfs"))
    
    # Now copy them over to Thin* because Cyan sucks.
    # NOTE: Yes, we will do on-demand downloads
    #       Updating the whole game at launch is stupid.
    if gotExt:
        shutil.copy(os.path.join("FileSrv", "External.mfs"), os.path.join("FileSrv", "ThinExternal.mfs"))
    if gotInt:
        shutil.copy(os.path.join("FileSrv", "Internal.mfs"), os.path.join("FileSrv", "ThinInternal.mfs"))


def make_new_preloader_mfs(src, key):
    def buf_to_int(str):
        val = 0
        val += (int(str[0], 16) * 0x10000000) + (int(str[1], 16) * 0x01000000)
        val += (int(str[2], 16) * 0x00100000) + (int(str[3], 16) * 0x00010000)
        val += (int(str[4], 16) * 0x00001000) + (int(str[5], 16) * 0x00000100)
        val += (int(str[6], 16) * 0x00000010) + (int(str[7], 16) * 0x00000001)
        return val
    
    def do_auth_file(path):
        rel = os.path.relpath(path, src)
        tmpfile = os.path.join(tmpdir, rel)
        handle = open(path, "rb")
        data = handle.read()
        handle.close()
        stream = plEncryptedStream()
        stream.open(tmpfile, fmCreate, plEncryptedStream.kEncDroid)
        stream.setKey(droid)
        stream.write(data)
        stream.close()
        line = do_file(rel, tmpdir)
        preloader.write(line)
        os.unlink(tmpfile)
    
    droid = []
    droid.append(buf_to_int(key[0:8]))
    droid.append(buf_to_int(key[8:16]))
    droid.append(buf_to_int(key[16:24]))
    droid.append(buf_to_int(key[24:32]))
    
    preloader = create_manifest("SecurePreloader")
    pydir = os.path.join(src, "Python")
    sdldir = os.path.join(src, "SDL")
    os.mkdir(os.path.join(tmpdir, "Python"))
    os.mkdir(os.path.join(tmpdir, "SDL"))
    dir = os.listdir(pydir)
    for entry in dir:
        path = os.path.join(pydir, entry)
        ext = os.path.splitext(path)[1]
        if not os.path.isfile(path):
            continue
        if ext != ".pak":
            continue
        do_auth_file(path)
    
    dir = os.listdir(sdldir)
    for entry in dir:
        path = os.path.join(sdldir, entry)
        ext = os.path.splitext(path)[1]
        if not os.path.isfile(path):
            continue
        if ext != ".sdl":
            continue
        do_auth_file(path)
    preloader.close()
    os.rmdir(os.path.join(tmpdir, "Python"))
    os.rmdir(os.path.join(tmpdir, "SDL"))

def make_old_preloader_mfs(src, key):
    # Lazy, so this support is in here too.
    # This is considerably more hacky than the rest of the script.
    def buf_to_int(str):
        val = 0
        val += (int(str[0], 16) * 0x10000000) + (int(str[1], 16) * 0x01000000)
        val += (int(str[2], 16) * 0x00100000) + (int(str[3], 16) * 0x00010000)
        val += (int(str[4], 16) * 0x00001000) + (int(str[5], 16) * 0x00000100)
        val += (int(str[6], 16) * 0x00000010) + (int(str[7], 16) * 0x00000001)
        return val
    
    
    def create_list(name):
        if not os.path.exists("AuthSrv"):
            os.mkdir("AuthSrv")
    
        file = open(os.path.join("AuthSrv", name + ".list"), "w+")
        return file
    
    
    def do_file_hax(file):
        realpath = os.path.join("AuthSrv", file)
        tomake = os.path.split(realpath)[0]
        if not os.path.exists(tomake):
            os.makedirs(tomake)
        
        handle = open(os.path.join(src, file), "rb")
        data = handle.read()
        handle.close()
        
        stream = plEncryptedStream()
        stream.open(realpath, fmCreate, plEncryptedStream.kEncDroid)
        stream.setKey(droid)
        stream.write(data)
        stream.close()
        
        # Note: / -> \ because Microsoft.
        stat = os.stat(realpath)
        line = "%s,%s" % (file.replace("/", "\\"), stat.st_size)
        print(line)
        
        return line + "\n"
    
    droid = []
    droid.append(buf_to_int(key[0:8]))
    droid.append(buf_to_int(key[8:16]))
    droid.append(buf_to_int(key[16:24]))
    droid.append(buf_to_int(key[24:32]))
    print(droid)
    
    pak = create_list("Python_pak")
    pydir = os.path.join("AuthSrv")
    
    test = os.path.join(src, "Python")
    dir = os.listdir(test)
    for entry in dir:
        path = os.path.join(test, entry)
        rel = os.path.relpath(path, src)
        
        #If it's not a file, then we obviously don't want it
        if not os.path.isfile(path):
            continue
        
        if entry[len(entry) - 4:].lower() == ".pak":
            pak.write(do_file_hax(rel))
    pak.close()
    
    sdl = create_list("SDL_sdl")
    test = os.path.join(src, "SDL")
    dir = os.listdir(test)
    for entry in dir:
        path = os.path.join(test, entry)
        rel = os.path.relpath(path, src)
        
        #If it's not a file, then we obviously don't want it
        if not os.path.isfile(path):
            continue
        
        if entry[len(entry) - 4:].lower() == ".sdl":
            sdl.write(do_file_hax(rel))
    sdl.close()


def make_patcher_mfs(src):
    il = os.path.join(src, "plUruLauncher.exe")
    el = os.path.join(src, "UruExplorer.exe")
    si = do_file("server.ini", src, "Patcher")
    
    if os.path.isfile(il):
        internal = create_manifest("InternalPatcher")
        internal.write(do_file("plUruLauncher.exe", src, "Patcher"))
        internal.write(si)
        internal.close()
    
    if os.path.isfile(el):
        external = create_manifest("ExternalPatcher")
        external.write(do_file("UruLauncher.exe", src, "Patcher"))
        external.write(si)
        external.close()


if __name__ == "__main__":
    plDebug.InitFile()
    (options, args) = parser.parse_args()
    
    # Make a complete file server?
    if options.complete:
        make_patcher_mfs(options.source)
        make_client_mfs(options.source)
        make_new_preloader_mfs(options.source, options.droid)
        make_all_age_mfs(options.source)
    else:
        # Let's see if we're making a client manifest
        test = options.age.replace("Thin", "")
        if test == "External" or test == "Internal":
            make_client_mfs(options.source)
        elif options.age == "ExternalPatcher" or options.age == "InternalPatcher" or options.age == "Patcher":
            make_patcher_mfs(options.source)
        elif options.age == "InsecurePreloader":
            # This is the new, testing SecurePreloader replacement
            # The pfSecurePreloader will (eventually) look for this
            # MFS first and use it as a priority to cache the Python & SDL
            make_new_preloader_mfs(options.source, options.droid)
        elif options.age == "SecurePreloader":
            # This is the old pfSecurePreloader generator
            # You'll want to provide the droid key.
            # Also, we don't magically pack the python for you
            # We're LAZY, after all.
            make_old_preloader_mfs(options.source, options.droid)
        else:
            make_age_mfs(options.age, options.source)
    os.rmdir(tmpdir)
