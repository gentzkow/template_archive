### ENVIRONMENT
import git
import imp
import os
import yaml

ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir 
f, path, desc = imp.find_module('gslab_make', [os.path.join(ROOT, 'lib')]) 
gs = imp.load_module('gslab_make', f, path, desc)

PATHS = { # Set default paths; used by `gslab_make` functions
    'config_user'     : '../config_user.yaml',
    'input_dir'       : 'input', 
    'external_dir'    : 'external',
    'output_dir'      : 'output/',
	'output_local_dir': [],                     # Optional; include any local directories with outputs
    'pdf_dir'         : 'output/',
    'makelog'         : 'log/make.log',         # Set to '' to avoid writing log
    'output_statslog' : 'log/output_stats.log', # Set to '' to avoid writing log
    'output_headslog' : 'log/output_heads.log', # Set to '' to avoid writing log
    'link_maplog'     : 'log/link_map.log',     # Set to '' to avoid writing log
    'link_statslog'   : 'log/link_stats.log',   # Set to '' to avoid writing log
    'link_headslog'   : 'log/link_heads.log'    # Set to '' to avoid writing log
}

PATH_MAPPINGS = { # Set path mappings; used by `create_links` functions
    'root': ROOT
}

### CONFIG USER 
config_user = yaml.load(open(PATHS['config_user'], 'rb'))
if config_user['local']['executables']: # Update executables; used by `run_program` functions
    gs.private.metadata.default_executables[os.name].update(config_user['local']['executables'])
if config_user['external']: # Update path mappings; used by `create_links` functions
    PATH_MAPPINGS.update(config_user['external'])

### START 
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

### GET INPUT FILES 
inputs = gs.create_input_links(PATHS, ['inputs.txt'], PATH_MAPPINGS)
externals = gs.create_external_links(PATHS, ['externals.txt'], PATH_MAPPINGS)
gs.write_link_logs(PATHS, inputs + externals)
gs.get_modified_links(PATHS, inputs + externals)

### RUN SCRIPTS
gs.run_python(PATHS, program = 'code/descriptive.py')

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### END
gs.end_makelog(PATHS)