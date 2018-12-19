#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
        
######################################################
# Define Messages
######################################################      
    
# 1) Critical Errors
crit_error_unknown_system = 'ERROR! Only the following operating systems are supported: `POSIX`, `NT`' 
crit_error_no_makelog = 'ERROR! Makelog `%s` not found (either not started or deleted after started)' 
crit_error_no_file = 'ERROR! File `%s` not found' 
crit_error_no_files = 'ERROR! Files `%s` not found'
crit_error_no_path = 'ERROR! Path `%s` not found' 
crit_error_no_path_wildcard = 'ERROR! Paths matching `%s` not found' 
crit_error_bad_command = 'ERROR! Command `%s` cannot be executed by operating system' 
crit_error_bad_link = 'ERROR! Link `%s` incorrectly specified (check if tab-delimited)' 
crit_error_extension = 'ERROR! `%s` does not have the right program extension' 
crit_error_path_mapping = 'ERROR! `{%s}` found in linking instructions but not in path mapping'

# 2) Syntax Errors
syn_error_wildcard = 'ERROR! Symlink and target must have same number of wildcards' 
syn_error_options = 'ERROR! Duplicate options specified' 

# 3) Type errors
type_error_file_list = 'ERROR! Files must be specified in a list' 
type_error_not_dir = 'ERROR! Path `%s` is not a directory' 

# 4) Notes & Warnings
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '
note_dash_line = '-' * 80
note_star_line = '*' * 80 