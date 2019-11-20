#!/usr/bin/env python

import sys
import os
import glob
import re

if len(sys.argv) == 1:
    print("""
    Invoke thusly: find . -name "*.c" -print0 | xargs -0 -n 1 python3 auto_build.py
    """)

cwd = os.getcwd()

cfname = 'shapes2.c'

USE_DOCKER_FOR_WKHTML = True

buildTemplate = 'docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc gcc -Wall -lm "%s" >> ./output/checks.txt 2>&1'
execTemplate = 'echo %s | docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc timeout 2 ./a.out | head -c 5000 >> ./output/checks.txt 2>&1'
highlightTemplate = 'docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc highlight "%s" -l -d ./output -V'
wkhtmlTemplate = 'docker run --rm -i -v "$PWD":/work -v /work/fonts -log-driver=none -a stdin -a stdout -a stderr checkc wkhtmltopdf ./output/*.c.html ./output/checks.html %s.pdf'

prefix = """
<html>
<head>
<style>
@font-face {
    font-family: mono;
    src: url('file:///work/fonts/DroidSansMono.ttf');
}
</style>
</head>
<body>
<pre style="font-family: mono;">
"""

postfix = """
</pre>
</body>
</html>
"""

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

    codeDir = '/'.join(blocks[:-1])
    
    os.chdir(os.path.join(cwd, codeDir))
    print("Checking %s" % codeDir)
    os.system('mkdir ./output')
    os.system('echo "Compile Output:" > ./output/checks.txt')
    cmd = buildTemplate % fname
    print("building:", cmd)
    os.system(cmd)

    os.system('echo "Compile Output Complete" >> ./output/checks.txt')
    if (fname == cfname):
        os.system('echo filename is %s >> ./output/checks.txt' % fname)
    else:
        os.system('echo filename is %s, not %s | head -100 >> ./output/checks.txt' % (fname, cfname))

    cmd = highlightTemplate % fname
    print("execing highlight:", cmd)
    os.system(cmd)

    args = ((1,9,6), (2,8,12), (3,10,7), (4,8), (5,12,7), (6,10), (7,9), (8,8), (9,10))
    
    for t in args:
        print("Testing args:", t)
        os.system("echo %s >> ./output/checks.txt" % ("Testing args:" + ' '.join([str(x) for x in t])))
        cmd = execTemplate % ' '.join([str(x) for x in t])
        print("execing: %s" % cmd)
        os.system(cmd)

    print("building PDF")

    if USE_DOCKER_FOR_WKHTML:
        #
        # create pre-formatted HTML file with mono font installed to fix debian wkhtmltopdf problem.
        #
        fo = open('./output/checks.html','w')
        fo.write(prefix)
        fi = open('./output/checks.txt')
        fo.write(fi.read())
        fi.close()
        fo.write(postfix)
        fo.close()
        
        cmd = wkhtmlTemplate % username
        print("Execing: %s" % cmd)
        os.system(cmd)
        os.system('mv %s.pdf %s/.' % (username, cwd))
        
    else:
        os.system('wkhtmltopdf ./output/*.html ./output/*.txt %s/%s.pdf' % (cwd, username))

    os.chdir(cwd)
