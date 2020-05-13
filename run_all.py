###################
### ENVIRONMENT ###
###################
import git
import imp
import os

### SET DEFAULT PATHS
ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir 

PATHS = {
    'root'        : ROOT,
    'lib'         : os.path.join(ROOT, 'lib'),
    'config_user' : os.path.join(ROOT, 'config_user.yaml')
}

### LOAD GSLAB MAKE
f, path, desc = imp.find_module('gslab_make', [PATHS['lib']]) 
gs = imp.load_module('gslab_make', f, path, desc)

### LOAD CONFIG USER 
gs.update_executables(PATHS)

###########
### RUN ###
###########

### RUN SCRIPTS
gs.run_module(root = ROOT, module = 'data')
gs.run_module(root = ROOT, module = 'analysis')
gs.run_module(root = ROOT, module = 'paper_slides')