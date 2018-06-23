#! /usr/bin/env python

import subprocess, shutil, os
import gslab_make as gs

for dir in ['output', 'temp']:
    shutil.rmtree(dir, ignore_errors='true')
    os.mkdir(dir)
os.chdir('code')

gs.start_make_logging()

# GET EXTERNAL INPUT FILES
os.system('rsync -v ../../data/output/data.txt ../input')


# RUN SCRIPTS
gs.run_python(program = 'descriptive.py')

gs.end_make_logging()
raw_input('\n Press <Enter> to exit.')
