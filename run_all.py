###################
### ENVIRONMENT ###
###################
import git
import imp
import os
import yaml

# LOAD GSLAB MAKE
ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir 
f, path, desc = imp.find_module('gslab_make', [os.path.join(ROOT, 'lib')]) 
gs = imp.load_module('gslab_make', f, path, desc)

# SET DEFAULT PATHS
PATHS = {
    'makelog': ''
}

###########
### RUN ###
###########

### RUN SCRIPTS
os.chdir(ROOT + '/data')
gs.run_python(PATHS, program = 'make.py')

os.chdir(ROOT + '/analysis')
gs.run_python(PATHS, program = 'make.py')

os.chdir(ROOT + '/paper_slides')
gs.run_python(PATHS, program = 'make.py')