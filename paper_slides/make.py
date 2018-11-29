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

# FILL TABLES
gs.tablefill(template = 'code/tables.lyx', 
             input = 'input/tables.txt', 
             output = 'output/tables_filled.lyx')

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