#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
        
######################################################
# Define Messages
######################################################      
    
# 1) Critical Errors
crit_error_unknown_system = 'ERROR! Only the following operating systems are supported: `POSIX`, `NT`.' 
crit_error_no_makelog = 'ERROR! Makelog `%s` not found. Makelog either not started (via `start_makelog`) or deleted after started.' 
crit_error_no_program_output = 'ERROR! Certain applications (`matlab`, `sas`, `stata`) automatically create program outputs when ran using system command. Program output `%s` is expected from `%s` but cannot be not found or opened. Traceback can be found below.'
crit_error_no_file = 'ERROR! File `%s` not found.' 
crit_error_no_files = 'ERROR! Files matching `%s` not found.'
crit_error_no_path = 'ERROR! Path `%s` not found.' 
crit_error_no_path_wildcard = 'ERROR! Paths matching `%s` not found.' 
crit_error_bad_command = 'ERROR! Command `%s` cannot be executed by operating system. Command may be misspecified or does not exist. Traceback can be found below.' 
crit_error_bad_move = 'ERROR! Link/copy `%s` incorrectly specified. Link/copy should be specified in the following formats: `destination | source` for inputs. Traceback can be found below.' 
crit_error_extension = 'ERROR! Program `%s` does not have correct extension. Program should have one of the following extensions: %s.' 
crit_error_path_mapping = 'ERROR! `{%s}` found in linking/copying instructions but not in path mapping. Traceback can be found below.'
crit_error_no_repo = 'ERROR! Current working directory is not part of a git repository.'

# 2) Syntax Errors
syn_error_wildcard = 'ERROR! Symlink and target must have same number of wildcards (`*`).' 

# 3) Type errors
type_error_file_list = 'ERROR! Files `%s` must be specified in a list.' 
type_error_dir_list = 'ERROR! Directories `%s` must be specified in a list.' 
type_error_not_dir = 'ERROR! Path `%s` is not a directory.' 

# 4) Warnings
warning_glob = 'WARNING! No files were returned by `glob_recursive` for path `%s` when walking to a depth of `%s`.'
warning_lyx_type = 'WARNING! Document type `%s` unrecognized. Reverting to default of no special document type.'
warning_modified_files = "WARNING! The following target files have been modified according to git status:\n%s"
warning_git_file = "WARNING! There exists files tracked by git larger than the config suggested limit (%s MB)." 
warning_git_repo = "WARNING! Total size of files tracked by git larger than the config suggested limit (%s MB)."
warning_git_lfs_file = "WARNING! There exists files tracked by git lfs larger than the config suggested limit (%s MB)."
warning_git_lfs_repo = "WARNING! Total size of files tracked by git lfs larger than the config suggested limitt (%s MB)."

# 5) Notes
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '

note_dash_line = '-' * 80
note_star_line = '*' * 80 