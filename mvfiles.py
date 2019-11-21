#!/usr/bin/env python

import sys
import os
import glob
import re

if len(sys.argv) == 1:
    print("""
    Invoke thusly: find . -name "*.c" -print0 | xargs -0 -n 1 python3 auto_build.py
    or:  python3 auto_build.py ./Name(username)/Submissions/foo.c
    """)

cwd = os.getcwd()

print("Got argv:", sys.argv)

for fpath in sys.argv[1:]:
    print("fpath = ", fpath)
    blocks = fpath.split('/')
    print("Found blocks:", blocks)
    fname = blocks[-1]
    print("Searching for username in ", blocks[1])
    userRE = re.compile("\((.+)\)")
    m = userRE.search(blocks[1])
    username = m.group(1)
    print("found username:", username)
    dstDir = os.path.join(cwd,os.path.join('moss',username))
    cmd = 'mkdir -p "%s"' % dstDir
    print("Executing: ", cmd)
    os.system(cmd)
    codeDir = '/'.join(blocks[:-1])
    srcDir = os.path.join(cwd, codeDir)
    cmd = 'mv "%s" "%s"' % (os.path.join(srcDir,fname), os.path.join(dstDir, fname))
    print("Executing: ", cmd)
    os.system(cmd)
    os.chdir(cwd)
