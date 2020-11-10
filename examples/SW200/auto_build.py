#!/usr/bin/env python

import sys
import os
import glob
import re
import datetime

if len(sys.argv) == 1:
    print("""
    Invoke thusly:  ls -1d proj-03-201/reports/* | xargs -n 1 python auto_build.py
    """)

"""
Typical path: proj-03-201/reports/mcbride_noah_mcbriden
"""

#
#     print("times:", sorted([datetime.datetime.strptime(x[7:-4],'%Y-%m-%d-%H:%M:%S-UTC') for x in map(lambda s: s.split('/')[3],reports)]))
#
cwd = os.getcwd()

USE_DOCKER_FOR_WKHTML = True

buildTemplate = 'docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc gcc -Wall -lm "%s" >> ./output/checks.txt 2>&1'
execTemplate = '%s | docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc timeout 5 ./a.out %s  > %s 2>&1'
vgExecTemplate = '%s | docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc timeout 5 valgrind ./a.out %s > %s 2>&1'
echoTemplate = 'echo "%s" >> ./output/checks.txt'
cmpTemplate = '../../ppmDIff %s %s %d >> ./output/checks.txt'
highlightTemplate = 'docker run --rm -i -v "$PWD":/work --log-driver=none -a stdin -a stdout -a stderr checkc highlight "%s" -l -d ./output -V'
pandocTemplate = 'docker run --rm -i -v "$PWD":/work -log-driver=none -a stdin -a stdout -a stderr checkc pandoc %s -o ./output/%s.html'
wkhtmlTemplate = 'docker run --rm -i -v "$PWD":/work -v /work/fonts -log-driver=none -a stdin -a stdout -a stderr checkc wkhtmltopdf --enable-local-file-access ./output/*.html %s.pdf'

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
    project, reports, reportdir = blocks = fpath.split('/')
    print("Found blocks:", blocks)
    bits = reportdir.split('_')
    last, first = bits[0], bits[1]
    studentName = first.capitalize() + ' ' + last.capitalize()
    username = bits[2]
    print("Student Name:", studentName)
    print("username", username)
    reports = glob.glob(fpath + '/*.txt') # typical timestamps -> '2020-09-16-23:47:51-UTC'
    lastReport = '/'.join(sorted(reports)[-1].split('/')[-2:])
    print("lastReport =", lastReport)
    
    codeDir = f"{blocks[0]}/submissions/{blocks[2]}"
    os.chdir(os.path.join(cwd, codeDir))

    print("Checking %s" % codeDir)
    os.system('mkdir ./output')

    # copy report to output
    cmd = "cp ../../reports/{0:s} ./output/{1:s}".format(lastReport,lastReport.split('/')[-1])
    print("executing ", cmd)
    os.system(cmd)
    print("Report:", lastReport, "copied")
    
    jsSrcs = glob.glob('src/**/*.js', recursive=True) 
    features = glob.glob('features/*.feature')
    
    print("srcs:", jsSrcs, features)
    
    for fname in jsSrcs:
        cmd = highlightTemplate % fname
        print("execing highlight:", cmd)
        os.system(cmd)
        
    for fname in glob.glob('*.md'):
        cmd = (pandocTemplate % (fname, fname))
        print("execing pandoc:", cmd)
        os.system(cmd)
        
    for fname in features:
        cmd = 'cp {0:s} ./output/{1:s}.txt'.format(fname, fname.split('/')[-1])
        print("execing:", cmd)
        os.system(cmd)

    if USE_DOCKER_FOR_WKHTML:
        #
        # create pre-formatted HTML file with mono font installed to fix debian wkhtmltopdf problem.
        #
        print("creating html for txt files")
        for txtPath in glob.glob('./output/*.txt'):
            outputPath = '.'.join(txtPath.split('.')[:-1] + ['html'])
            fo = open(outputPath,'w')
            fo.write(prefix)
            fi = open(txtPath)
            s = fi.read()
            fo.write(s.replace(chr(10003),'&#10003;'))
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

    print("----")
