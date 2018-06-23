#! /usr/bin/env python

import subprocess, shutil, os
import gslab_make as gs
import gslab_fill

for dir in ['output']:
    shutil.rmtree(dir, ignore_errors='true')
    os.mkdir(dir)
os.chdir('code')

gs.start_make_logging()

# GET EXTERNAL INPUT FILES
os.system('rsync -v ../../analysis/output/plot.eps ../input')
os.system('rsync -v ../../analysis/output/tables.txt ../input')

# FILL TABLES
gslab_fill.tablefill(template = 'tables.lyx', input = '../input/tables.txt', output = '../output/tables_filled.lyx')

# RUN SCRIPTS
gs.run_lyx(program = 'paper.lyx')
gs.run_lyx(program = 'online_appendix.lyx')
gs.run_lyx(program = 'slides.lyx')
gs.run_lyx(program = 'ondeck.lyx')
gs.run_lyx(program = 'text.lyx')
gs.run_latex(program = 'text.tex')

asdfsa

gs.end_make_logging()
raw_input('\n Press <Enter> to exit.')
