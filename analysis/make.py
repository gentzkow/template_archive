#! /usr/bin/env python

import shutil, os
import gslab_make as gs

for dir in ['output', 'input', 'temp']:
    shutil.rmtree(dir, ignore_errors='true')
    os.mkdir(dir)
os.chdir('code')

gs.start_make_logging()

# GET EXTERNAL INPUT FILES
os.symlink('../../data/output/data.txt', '../input/data.txt')

# RUN SCRIPTS
gs.run_python(program = 'descriptive.py')

gs.end_make_logging()
raw_input('\n Press <Enter> to exit.')
