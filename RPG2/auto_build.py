#!/usr/bin/env python

"""
Invoke thusly: find . -name "*.c" -print0 | xargs -0 -n 1 python foo.py
"""

import sys
import os
import glob
import re

cwd = os.getcwd()

"""
./Wilson, Jaedon(jawilson)/Submission attachment(s)/shapeCalculator.c
./Croxford, Emma(croxforde)/Submission attachment(s)/rpgl.c
./Gamache, Nolan(gamachen)/Submission attachment(s)/rpg1.c
./Bixler, Andrew(bixleraj)/Submission attachment(s)/rpg1.c
"""

for fpath in sys.argv[1:]:
    blocks = fpath.split('/')
    fname = blocks[-1]

    userRE = re.compile("\((.+)\)")
    m = userRE.search(blocks[1])
    username = m.group(1)
    
    codeDir = '/'.join(blocks[:-1])
    
    os.chdir(os.path.join(cwd, codeDir))
    print("Checking %s" % codeDir)
    os.system('mkdir ./output')
    os.system('echo "Compile Output:" > ./output/checks.txt')
    os.system('gcc -Wall "%s" >> ./output/checks.txt 2>&1 ' % fname)
    os.system('highlight "%s" -l -d ./output/ -V' % fname)
    os.system('echo "Compile Output Complete" >> ./output/checks.txt')
    if (fname == 'rpg2.c'):
        os.system('echo filename is %s >> ./output/checks.txt' % fname)
    else:
        os.system('echo filename is %s, not rpg2.c >> ./output/checks.txt' % fname)
    os.system('echo `grep -c printf %s` occurances of printf >> ./output/checks.txt' % fname)
    os.system('echo `grep -c scanf %s` occurances of scanf >> ./output/checks.txt' % fname)
    os.system('echo `grep -c rand %s` occurances of rand >> ./output/checks.txt' % fname)
    os.system('echo `grep -c while %s` occurances of while >> ./output/checks.txt' % fname)
    os.system('echo `grep -c for %s` occurances of for >> ./output/checks.txt' % fname)
    os.system('wkhtmltopdf ./output/*.html ./output/*.txt %s/%s.pdf' % (cwd, username))

"""
        os.chdir(os.path.join(cwd, dir))
        print("checking ", dir)
        os.system('yarn test > output/test.out.txt 2>&1 ')
        os.system('yarn lint > output/lint.out.txt 2>&1 ')
        cmd = "pandoc README.md -o ./output/README.html"
        print("executing: '" + cmd + "'")
        os.system(cmd)

        os.system('highlight ./src/*.ts ./tests/*.ts -l -d output/ -V')
        os.system('wkhtmltopdf ./output/*.html ./output/*.txt %s.pdf' % dir)
        os.chdir(cwd)

"""
