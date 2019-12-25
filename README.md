CheckC: formatting programs submitted to Ace for grading
========================================================

The idea is to create a flexible docker container that can be used to
portably format student submitted work (through Ace) into a PDF
that can be easily graded.

You can "download assignments" from Ace. You'll get a .zip which can be
expanded into a folder that contains one sub-folder for each student:

    .
    ├── A,\ Student(aemail)
    │   ├── Feedback\ Attachment(s)
    │   ├── Submission\ attachment(s)
    │   │   └── filea.c
    │   ├── comments.txt
    │   └── timestamp.txt
    ├── B,\ Student(bemail)
    │   ├── Feedback\ Attachment(s)
    │   ├── Submission\ attachment(s)
    │   │   └── fileb.c
    │   ├── comments.txt
    │   └── timestamp.txt
    └── grades.csv

The program `auto_build.py` traverses this directory structure, builds executables, executes them and stores the output in a way that can be converted into a PDF for hand grading. There is always some customization required based on the inputs/outputs but this is a reasonable starting point.

