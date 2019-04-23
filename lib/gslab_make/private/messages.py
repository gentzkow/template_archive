#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
        
######################################################
# Define Messages
######################################################      
    
# 1) Critical Errors
crit_error_unknown_system = '\nERROR! Only the following operating systems are supported: `POSIX`, `NT`.' 
crit_error_no_makelog = '\nERROR! Makelog `%s` not found. Makelog either not started (via `start_makelog`) or deleted after started.' 
crit_error_no_program_output = '\nERROR! Certain applications (`matlab`, `sas`, `stata`) automatically create program outputs when ran using system command. Program output `%s` is expected from `%s` but cannot be not found or opened. Traceback can be found below.'
crit_error_no_file = '\nERROR! File `%s` not found.' 
crit_error_no_files = '\nERROR! Files matching `%s` not found.'
crit_error_no_path = '\nERROR! Path `%s` not found.' 
crit_error_no_path_wildcard = '\nERROR! Paths matching `%s` not found.' 
crit_error_bad_command = '\nERROR! Command `%s` cannot be executed by operating system. Command may be misspecified or does not exist. Traceback can be found below.' 
crit_error_bad_move = '\nERROR! Link/copy `%s` incorrectly specified. Link/copy should be specified in the following format: `destination | source`. Traceback can be found below.' 
crit_error_move_command = '\nERROR! Command `%s` cannot be executed by operating system. Check permissions and if on Windows, run as administrator. Traceback can be found below.'
crit_error_extension = '\nERROR! Program `%s` does not have correct extension. Program should have one of the following extensions: %s.' 
crit_error_path_mapping = '\nERROR! `{%s}` found in linking/copying instructions but not in path mapping. Traceback can be found below.'
crit_error_no_repo = '\nERROR! Current working directory is not part of a git repository.'

# 2) Syntax Errors
syn_error_wildcard = '\nERROR! Symlink and target must have same number of wildcards (`*`).' 

# 3) Type errors
type_error_file_list = '\nERROR! Files `%s` must be specified in a list.' 
type_error_dir_list = '\nERROR! Directories `%s` must be specified in a list.' 
type_error_not_dir = '\nERROR! Path `%s` is not a directory.' 

# 4) Warnings
warning_glob = 'WARNING! No files were returned by `glob_recursive` for path `%s` when walking to a depth of `%s`.'
warning_lyx_type = 'WARNING! Document type `%s` unrecognized. Reverting to default of no special document type.'
warning_modified_files = "WARNING! The following target files have been modified according to git status:\n%s"
warning_git_file_print = "\nWARNING! Certain files tracked by git exceed config limit (%s MB). See logs for more detail." 
warning_git_file_log = "\nWARNING! Certain files tracked by git that exceed config limit (%s MB). See below for list of files." 
warning_git_repo = "\nWARNING! Total size of files tracked by git exceed config limit (%s MB)."
warning_git_lfs_file_print = "\nWARNING! Certain files tracked by git lfs exceed config limit (%s MB). See logs for more detail."
warning_git_lfs_file_log = "\nWARNING! Certain files tracked by git lfs exceed config limit (%s MB). See below for list of files."
warning_git_lfs_repo = "\nWARNING! Total size of files tracked by git lfs exceed config limitt (%s MB)."

# 5) Notes
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '

note_dash_line = '-' * 80