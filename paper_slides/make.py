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
    'config'          : '../config.yaml',
    'config_user'     : '../config_user.yaml',
    'input_dir'       : 'input', 
    'external_dir'    : 'external',
    'output_dir'      : 'output/',
    'output_local_dir': [],                     # Optional; include any local directories with outputs
    'pdf_dir'         : 'output/',
    'makelog'         : 'log/make.log',         # Set to '' to avoid writing log
    'output_statslog' : 'log/output_stats.log', # Set to '' to avoid writing log
    'output_headslog' : 'log/output_heads.log', # Set to '' to avoid writing log
    'source_maplog'   : 'log/source_map.log',   # Set to '' to avoid writing log
    'source_statslog' : 'log/source_stats.log', # Set to '' to avoid writing log
    'source_headslog' : 'log/source_heads.log'  # Set to '' to avoid writing log
}

### SET PATH MAPPINGS
PATH_MAPPINGS = { 
    'root': ROOT
}

### LOAD CONFIG USER 
gs.update_executables(PATHS)
PATH_MAPPINGS = gs.update_mappings(PATHS, PATH_MAPPINGS)

############
### MAKE ###
############

### START MAKE
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

### GET INPUT FILES 
inputs = gs.copy_inputs(PATHS, ['input.txt'], PATH_MAPPINGS)
externals = gs.copy_externals(PATHS, ['external.txt'], PATH_MAPPINGS)
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

### FILL TABLES
gs.tablefill(template = 'code/tables.lyx', 
             input    = 'input/tables.txt', 
             output   = 'output/tables_filled.lyx')

### RUN SCRIPTS
gs.run_lyx(PATHS, program = 'code/paper.lyx')
gs.run_lyx(PATHS, program = 'code/online_appendix.lyx')
gs.run_lyx(PATHS, program = 'code/slides.lyx')
gs.run_lyx(PATHS, program = 'code/ondeck.lyx')
gs.run_lyx(PATHS, program = 'code/text.lyx')

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### CHECK FILE SIZES
gs.check_module_size(PATHS)

### END MAKE
gs.end_makelog(PATHS)