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

cfname = 'ppmproc.c'

USE_DOCKER_FOR_WKHTML = True

buildTemplate = 'docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc gcc -Wall -lm "%s" >> ./output/checks.txt 2>&1'
execTemplate = '%s | docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc timeout 5 ./a.out %s  > %s 2>&1'
vgExecTemplate = '%s | docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc timeout 5 valgrind ./a.out %s > %s 2>&1'
echoTemplate = 'echo "%s" >> ./output/checks.txt'
cmpTemplate = '../../ppmDIff %s %s %d >> ./output/checks.txt'
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
    
    os.system('echo "Filename check:" >> ./output/checks.txt')
    
    if (fname == cfname):
        os.system('echo filename is %s >> ./output/checks.txt' % fname)
    else:
        os.system('echo filename is %s, not %s | head -100 >> ./output/checks.txt' % (fname, cfname))

    cmd = highlightTemplate % fname
    print("execing highlight:", cmd)
    os.system(cmd)

    for items in [('1 25',1), ('2',1), ('3 100',1), ('4',1), ('5',2)]:
        fAbbrev = '-'.join(items[0].split())
        imFile = 'out' + fAbbrev + '.ppm'
        cmpFile = '../../test' + fAbbrev + '.ppm'
        cmd = execTemplate % ('cat ~/Desktop/test.ppm', items[0], imFile)
        print("execing: %s" % cmd)
        os.system(cmd)
        cmd = echoTemplate % ('checking arguments: ' + items[0])
        print("execing: %s" % cmd)
        os.system(cmd)
        cmd  = cmpTemplate % (imFile, cmpFile, items[1])
        print("execing: %s" % cmd)
        os.system(cmd)

    cmd = echoTemplate % ('running big image test: ' + items[0])
    print("execing: %s" % cmd)
    os.system(cmd)
    cmd = execTemplate % ('cat ~/Desktop/flower.ppm', '3 100', 'outBig.ppm')
    print("execing: %s" % cmd)
    os.system(cmd)
    os.system('echo check output filesize: >> ./output/checks.txt')
    os.system('wc -l outBig.ppm >> ./output/checks.txt')

    os.system('echo valgrind check >> ./output/checks.txt')
    cmd = vgExecTemplate % ('cat ~/Desktop/test.ppm', '3 100', 'outVg.ppm')
    print("execing: %s" % cmd)
    os.system(cmd)
    os.system('cat outVg.ppm >> ./output/checks.txt')

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
