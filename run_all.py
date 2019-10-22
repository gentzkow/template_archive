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

###########
### RUN ###
###########

### RUN SCRIPTS
gs.run_module(root = ROOT, module = 'data')
gs.run_module(root = ROOT, module = 'analysis')
gs.run_module(root = ROOT, module = 'paper_slides')