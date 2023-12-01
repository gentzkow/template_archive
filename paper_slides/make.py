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
inputs = gs.copy_inputs(PATHS, ['input.txt'])
externals = gs.copy_externals(PATHS, ['external.txt'])
gs.write_source_logs(PATHS, inputs + externals)
gs.get_modified_sources(PATHS, inputs + externals)

## MAKE VERSION LOGS
gs.write_version_logs(PATHS)

### FILL TABLES
gs.tablefill(template = 'code/tables.tex', 
             inputs   = 'input/regression.csv', 
             output   = 'output/tables_filled.tex')

### RUN SCRIPTS
gs.run_latex(PATHS, program = 'code/paper.tex')
gs.run_latex(PATHS, program = 'code/online_appendix.tex')
gs.run_latex(PATHS, program = 'code/slides.tex')
gs.export_excel_tables(PATHS, template = 'gs_primary', scalar = 'gs_primary_scalars.xlsx')
# gs.export_excel_tables(PATHS, template = 'gs_widetable', scalar = 'gs_widetable_scalars.xlsx')
# gs.export_excel_tables(PATHS, template = 'gs_longtable', scalar = 'gs_longtable_scalars.xlsx')
# gs.export_excel_tables(PATHS, template = 'gs_widetable_extreme', scalar = 'gs_widetable_extreme_scalars.xlsx')
# gs.export_excel_tables(PATHS, template = 'gs_longtable_extreme', scalar = 'gs_longtable_extreme_scalars.xlsx')
gs.quit_excel(PATHS)

### LOG OUTPUTS
gs.log_files_in_output(PATHS)

### CHECK FILE SIZES
gs.check_module_size(PATHS)

### END MAKE
gs.end_makelog(PATHS)
