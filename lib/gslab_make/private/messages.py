# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

        
# ~~~~~~~~~~~~~~~ #
# Define messages #
# ~~~~~~~~~~~~~~~ #  
    
# Critical errors
crit_error_unknown_system = \
    '\nERROR! Your operating system `%s` is unknown. `gslab_make` only supports the following operating systems: `posix`, `nt`.' 
crit_error_no_makelog = \
    '\nERROR! Makelog `%s` cannot be found. ' + \
    'This could be for the following reasons:\n' + \
    '- Makelog was not started (via `start_makelog`)\n' + \
    '- Makelog ended (via `end_makelog`) prematurely\n' + \
    '- Makelog deleted or moved after started'
    
# ACTION ITEM: `end_makelog` CURRENTLY DOESN'T ACTUALLY TURN MAKE LOG STATUS OFF
    
crit_error_no_program_output = \
    '\nERROR! Program output `%s` is expected from `%s` but cannot be found. ' + \
    'Certain applications (`matlab`, `sas`, `stata`) automatically create program outputs when run using system command. ' + \
    '`gslab_make` attempts to migrate these program outputs appropriately. ' + \
    'For further detail, refer to the traceback below.'
crit_error_no_key = \
    '\nERROR! Argument `paths` is missing a value for key `%s`. ' + \
    'Add a path for `%s` to your paths dictionary.'
crit_error_no_file = \
    '\nERROR! File `%s` cannot be found.'
crit_error_no_files = \
    '\nERROR! Files matching pattern `%s` cannot be found.'
crit_error_no_path = \
    '\nERROR! Path `%s` cannot be found.' 
crit_error_no_path_wildcard = \
    '\nERROR! Paths matching pattern `%s` cannot be found.' 
crit_error_no_attributes = \
    '\nERROR! Cannot open git attributes file for repository. Confirm that repository has git attributes file.'
crit_error_bad_command = \
    '\nERROR! The following command cannot be executed by operating system.\n' + \
    '  > %s\n' + \
    'This could be because the command may be misspecified or does not exist. ' + \
    'For further detail, refer to the traceback below.'
crit_error_bad_move = \
    '\nERROR! An error was encountered attempting to link/copy with the following instruction in file `%s`.\n' + \
    '  > %s\n' + \
    'Link/copy instructions should be specified in the following format:\n' + \
    '  > destination | source\n' + \
    'For further detail, refer to the traceback below.'
crit_error_move_command = \
    '\nERROR! The following command cannot be executed by operating system.\n' + \
    '  > %s\n' + \
    'Check permissions and if on Windows, run as administrator. ' + \
    'For further detail, refer to the traceback below.'
crit_error_extension = \
    '\nERROR! Program `%s` does not have correct extension. ' + \
    'Program should have one of the following extensions: %s.' 
crit_error_path_mapping = \
    '\nERROR! Argument `paths` is missing a value for key `%s`. ' + \
    '`{%s}` found in the following instruction in file `%s`.\n' + \
    '  > %s\n' + \
    'Confirm that your config user file contains an external dependency for {%s} and that it has been properly loaded (via `update_paths`). ' + \
    'For further detail, refer to the traceback below.'
crit_error_no_repo = \
    '\nERROR! Current working directory is not part of a git repository.'
crit_error_not_float = \
    '\nERROR! You are attempting to round or format a value (`%s`) that is not a number.'
crit_error_no_input_table = \
    '\nERROR! None of the inputs match the tab name for table `%s`.'
crit_error_not_enough_values = \
    '\nERROR! Not enough values in input for table `%s`.'
crit_error_too_many_values = \
    '\nERROR! Too many values in input for table `%s`.'
crit_error_no_tag = \
    '\nERROR! Input `%s` is missing a tab name.'

# Syntax errors
syn_error_wildcard = \
    '\nERROR! Destination and source must have same number of wildcards (`*`). ' + \
    'Fix the following instruction in file `%s`.\n' + \
    '  > %s'

# Type errors
type_error_file_list = \
    '\nERROR! Files `%s` must be specified as a list.' 
type_error_dir_list = \
    '\nERROR! Directories `%s` must be specified as a list.' 
type_error_not_dir = \
    '\nERROR! Path `%s` is not a directory.' 

# Warnings
warning_glob = \
    'WARNING! No files were found for path `%s` when walking to a depth of `%s`.'
warning_lyx_type = \
    'WARNING! Document type `%s` is unrecognized. ' + \
    'Reverting to default of no special document type.'
warning_modified_files = \
    'WARNING! The following target files have been modified according to git status:\n' + \
    '%s'
warning_git_file_print = \
    '\nWARNING! Certain files tracked by git exceed the config size limit (%s MB). ' + \
    'See makelog for list of files.' 
warning_git_file_log = \
    '\nWARNING! Certain files tracked by git exceed the config size limit (%s MB). ' + \
    'See below for list of files.' 
warning_git_repo = \
    '\nWARNING! Total size of files tracked by git exceed the repository config limit (%s MB).'
warning_git_lfs_file_print = \
    '\nWARNING! Certain files tracked by git-lfs exceed the config size limit (%s MB). ' + \
    'See makelog for list of files.'
warning_git_lfs_file_log = \
    '\nWARNING! Certain files tracked by git-lfs exceed the config size limit (%s MB). ' + \
    'See below for list of files.'
warning_git_lfs_repo = \
    '\nWARNING! Total size of files tracked by git-lfs exceed the repository config limit  (%s MB).'
warning_copy = \
    'To copy the following file, enter "Yes". Otherwise, enter "No". ' + \
    'Update any archives and documentation accordingly.\n' + \
    '> %s\n' + \
    'will be uploaded to\n' + \
    '> %s\n' + \
    'Input: '
warning_not_conda = \
    'WARNING! You are not in an active conda environment'
warning_old_conda = \
    'WARNING! setup/conda_env.yaml has been updated since you last updated your environment.'
# Notes
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '

note_dash_line = '-' * 80