###################
### ENVIRONMENT ###
###################
import git
import importlib
import os
import sys

### SET DEFAULT PATHS
ROOT = '..'

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
gs_path = os.path.join(PATHS['lib'], 'gslab_make', 'gslab_make', '__init__.py')
spec = importlib.util.spec_from_file_location('gslab_make', gs_path)
gs = importlib.util.module_from_spec(spec)
sys.modules['gslab_make'] = gs
spec.loader.exec_module(gs)

### LOAD CONFIG USER 
PATHS = gs.update_paths(PATHS)
gs.update_executables(PATHS)

# Check if running from root to check conda status
if len(sys.argv) < 2 or sys.argv[1] != 'run_all':
    gs.check_conda_status(root = ROOT)

############
### MAKE ###
############

### START MAKE
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

### GET INPUT FILES 
inputs = gs.link_inputs(PATHS, ['input.txt'])
externals = gs.link_externals(PATHS, ['external.txt'])
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

### RUN SCRIPTS
gs.run_python(PATHS, program = 'code/analyze_data.py')

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### CHECK FILE SIZES
gs.check_module_size(PATHS)

### END MAKE
gs.end_makelog(PATHS)