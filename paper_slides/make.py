# ENVIRONMENT
import git
import imp
import os
import yaml

ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir
f, path, desc = imp.find_module('gslab_make', [os.path.join(ROOT, 'lib', 'gslab_make')])
gs = imp.load_module('gslab_make', f, path, desc)

PATHS = {
    'config_user'     : '../config_user.yaml',
    'input_dir'       : 'input', 
    'external_dir'    : 'external',
    'output_dir'      : 'output/',
    'pdf_dir'         : 'output/',
    'makelog'         : 'log/make.log',
    'output_statslog' : 'log/output_stats.log',
    'output_headslog' : 'log/output_heads.log', 
    'link_maplog'     : 'log/link_map.log',
    'link_statslog'   : 'log/link_stats.log',
    'link_headslog'   : 'log/link_heads.log'
}

PATH_MAPPINGS = {
    'root': ROOT
}

# CONFIG USER
config_user = yaml.load(open(PATHS['config_user'], 'rb'))
if config_user['local']['executables']:
    gs.private.metadata.default_executables[os.name].update(config_user['local']['executables']) 
if config_user['external']:
    PATH_MAPPINGS.update(config_user['external'])

# START
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

# GET INPUT FILES
inputs = gs.create_input_links(PATHS, ['inputs.txt'], PATH_MAPPINGS)
externals = gs.create_external_links(PATHS, ['externals.txt'], PATH_MAPPINGS)
gs.write_link_logs(PATHS, inputs + externals)

# FILL TABLES
gs.tablefill(template = 'code/tables.lyx', 
             input    = 'input/tables.txt', 
             output   = 'output/tables_filled.lyx')

# RUN SCRIPTS
gs.run_lyx(PATHS, program = 'code/paper.lyx')
gs.run_lyx(PATHS, program = 'code/online_appendix.lyx')
gs.run_lyx(PATHS, program = 'code/slides.lyx')
gs.run_lyx(PATHS, program = 'code/ondeck.lyx')
gs.run_lyx(PATHS, program = 'code/text.lyx')

# LOG OUTPUTS
gs.log_files_in_output(PATHS)

# END
gs.end_makelog(PATHS)
raw_input('\n Press <Enter> to exit.')