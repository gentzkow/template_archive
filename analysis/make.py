###################
### ENVIRONMENT ###
###################
import os
import sys

### LOAD GSLAB MAKE
ROOT = '..'
gslm_path = os.path.join(ROOT, 'lib', 'gslab_make')

sys.path.append(gslm_path)
import gslab_make as gs

### PULL PATHS FROM CONFIG
PATHS = {
    'root': ROOT,
    'config': os.path.join(ROOT, 'config.yaml')
}
PATHS = gs.update_internal_paths(PATHS)

### LOAD CONFIG USER 
PATHS = gs.update_external_paths(PATHS)
gs.update_executables(PATHS)

############
### MAKE ###
############

### START MAKE
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

### MAKE LINKS TO INPUT AND EXTERNAL FILES
inputs = gs.link_inputs(PATHS, ['input.txt'])
externals = gs.link_externals(PATHS, ['external.txt'])
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

## MAKE VERSION LOGS
gs.write_version_logs(PATHS)

### RUN SCRIPTS
gs.run_python(PATHS, program = 'code/analyze_data.py')
#gs.run_julia(PATHS, program = 'code/plot.jl')

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### CHECK FILE SIZES
gs.check_module_size(PATHS)

### END MAKE
gs.end_makelog(PATHS)