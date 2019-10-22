###################
### ENVIRONMENT ###
###################
import git
import imp
import os

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
f, path, desc = imp.find_module('gslab_make', [PATHS['lib']]) 
gs = imp.load_module('gslab_make', f, path, desc)

### LOAD CONFIG USER 
PATHS = gs.update_paths(PATHS)
gs.update_executables(PATHS)

############
### MAKE ###
############

### START MAKE
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

### GET INPUT FILES 
inputs = gs.copy_inputs(PATHS, ['input.txt'])
externals = gs.copy_externals(PATHS, ['external.txt'])
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

### FILL TABLES
gs.tablefill(template = 'code/tables.lyx', 
             inputs   = 'input/tables.txt', 
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