###################
### ENVIRONMENT ###
###################
import importlib
import importlib.util
import os
import sys

### SET DEFAULT PATHS
ROOT = '.'

PATHS = {
    'root'        : ROOT,
    'lib'         : os.path.join(ROOT, 'lib'),
    'config_user' : os.path.join(ROOT, 'config_user.yaml')
}

### LOAD GSLAB MAKE
gs_path = os.path.join(PATHS['lib'], 'gslab_make', 'gslab_make', '__init__.py')
spec = importlib.util.spec_from_file_location('gslab_make', gs_path)
gs = importlib.util.module_from_spec(spec)
sys.modules['gslab_make'] = gs
spec.loader.exec_module(gs)

### LOAD CONFIG USER 
gs.update_executables(PATHS)
gs.check_conda_status(root = ROOT)

###########
### RUN ###
###########

### RUN SCRIPTS
gs.run_module(root = ROOT, module = 'data')
gs.run_module(root = ROOT, module = 'analysis')
gs.run_module(root = ROOT, module = 'paper_slides')
