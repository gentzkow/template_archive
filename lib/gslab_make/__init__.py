#!/usr/bin/python
# -*- coding: latin-1 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

"""
=======================================================
gslab_make: a library of make.py and LyX filling tools
=======================================================

Description:
`make.py` is a Python script that facilitates running programs in batch mode. 
`make.py` relies on functions in `gslab_make` which provide simple and 
efficient commands that are portable across Unix and Windows.

`gslab_make` also provides two functions for filling LyX templates with data. 
These are `tablefill` and `textfill`. Please see their docstrings for further
detail on their use and functionalities.

Prerequisites:
*  Python 2.7/3.7 installed and executable path is added to system path

To use functions in this library that call applications other than Python, 
you must have the application installed with its executable path added to the
system path or defined as an environment variable/symbolic link. 
This remark applies to: Matlab, Stata, Perl, Mathematica 8.0 (the math kernel 
path must be added to system path), StatTransfer, LyX, R, and SAS.

Notes:
*  Default parameters, options, and executables used in `make.py` scripts are 
   defined in `/private/metadata.py`. The file extensions associated with 
   various applications are also defined in this file. 
*  For further detail on functions in `gslab_make`, refer to their docstrings
   or the master documentation.
"""

# Import make tools
from gslab_make.check_repo import check_module_size, get_modified_sources
from gslab_make.modify_dir import remove_dir, clear_dir, unzip, zip_dir
from gslab_make.move_sources import (link_inputs, link_externals, 
                                     copy_inputs, copy_externals)
from gslab_make.run_program import (run_stata, run_matlab, run_perl, run_python, 
                                    run_jupyter, run_mathematica, run_stat_transfer, 
                                    run_lyx, run_r, run_sas, execute_command, run_module)
from gslab_make.make_utility import (update_executables, update_mappings, copy_output)
from gslab_make.write_logs import (start_makelog, end_makelog, write_to_makelog,
                                   log_files_in_output, write_stats_log, write_heads_log)
from gslab_make.write_source_logs import write_source_logs


# Import fill tools
from gslab_make.tablefill import tablefill
from gslab_make.textfill import textfill
