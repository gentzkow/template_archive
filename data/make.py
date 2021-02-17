###################
### ENVIRONMENT ###
###################
import git
import importlib
import os
import sys

### SET DEFAULT PATHS
ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir 

PATHS = {
    'root'             : ROOT,
    'lib'              : os.path.join(ROOT, 'lib'),
    'config'           : os.path.join(ROOT, 'config.yaml'),
    'config_user'      : os.path.join(ROOT, 'config_user.yaml'),
    'input_dir'        : 'input', 
    'external_dir'     : 'external',
    'output_dir'       : 'output',
    'output_local_dir' : 'output_local',
    'makelog'          : 'log/make.log',         
    'output_statslog'  : 'log/output_stats.log', 
    'source_maplog'    : 'log/source_map.log',  
    'source_statslog'  : 'log/source_stats.log',
}

### LOAD GSLAB MAKE
spec = importlib.util.spec_from_file_location('gslab_make', 
                                              os.path.join(PATHS['lib'], 'gslab_make', '__init__.py'))
gs = importlib.util.module_from_spec(spec)
sys.modules['gslab_make'] = gs
spec.loader.exec_module(gs)

### LOAD CONFIG USER 
PATHS = gs.update_paths(PATHS)
gs.update_executables(PATHS)

# Check if running from root to check conda status
if sys.argv[1] != 'run_all':
    gs.check_conda_status(root = ROOT)

############
### MAKE ###
############

### START MAKE
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
# gs.clear_dir(['temp']) # Uncomment for Stata scripts
gs.start_makelog(PATHS)

### GET INPUT FILES 
inputs = gs.link_inputs(PATHS, ['input.txt'])
externals = gs.link_externals(PATHS, ['external.txt'])
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

### RUN SCRIPTS
gs.run_python(PATHS, 'code/merge_data.py')
gs.run_python(PATHS, 'code/clean_data.py')

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### CHECK FILE SIZES
gs.check_module_size(PATHS)

### END MAKE
gs.end_makelog(PATHS)