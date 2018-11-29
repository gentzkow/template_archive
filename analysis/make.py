#! /usr/bin/env python

# ENVIRONMENT
import gslab_make as gs

PATHS = {
    'link_dir'        : 'input/',
    'temp_dir'        : 'temp/',
    'output_dir'      : 'output/',
    'pdf_dir'         : 'output/',
    'makelog'         : 'log/make.log',
    'output_statslog' : 'log/output_stats.log',
    'output_headslog' : 'log/output_heads.log', 
    'linklog'         : 'log/link.log', 
    'link_maplog'     : 'log/link_map.log',
    'link_statslog'   : 'log/link_stats.log',
    'link_headslog'   : 'log/link_heads.log'
}

# START
gs.clear_dir(['input', 'output', 'log'])
gs.start_makelog(PATHS)

# GET INPUT FILES
links = gs.create_links(PATHS, ['inputs.txt', 'externals.txt']) 
gs.write_link_logs(PATHS, links)

# RUN SCRIPTS
gs.run_python(PATHS, program = 'code/descriptive.py')

# LOG OUTPUTS
gs.log_files_in_output(PATHS)

# END
gs.end_makelog(PATHS)
raw_input('\n Press <Enter> to exit.')