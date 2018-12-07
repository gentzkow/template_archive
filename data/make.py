#! /usr/bin/env python

# ENVIRONMENT
import os
import yaml
import gslab_make as gs

PATHS = {
    'config_user'     : '../config_user.yaml',
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
print(links)
gs.write_link_logs(PATHS, links)

# RUN SCRIPTS
gs.run_r(PATHS, program = 'code/create_table_data.r')
gs.run_stata(PATHS, program = 'code/create_graph_data.do')

# LOG OUTPUTS
gs.log_files_in_output(PATHS)

# END
gs.end_makelog(PATHS)
raw_input('\n Press <Enter> to exit.')