#! /usr/bin/env python

import subprocess, shutil, os
import gslab_make as gs

for dir in ['output', 'temp']:
    shutil.rmtree(dir)
    os.mkdir(dir)
os.chdir('code')
gs.start_make_logging()

# GET_EXTERNALS
#get_externals('externals.txt')

# ANALYSIS
gs.run_stata(program = 'create_data.do')

gs.end_make_logging()

raw_input('\n Press <Enter> to exit.')
