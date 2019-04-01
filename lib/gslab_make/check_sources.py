#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import git
import traceback

from gslab_make.private.exceptionclasses import CritError
import gslab_make.private.messages as messages
from gslab_make.private.utility import norm_path, format_error, glob_recursive
from gslab_make.write_logs import write_to_makelog
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

def get_git_status(repo): 
    """ Get git status.
    
    Parameters
    ----------
    repo : git.Repo 
        Git repository to show working tree status.

    Returns
    -------
    file_list : list
        List of changed files in git repository according to git status.
    """
    
    root = repo.working_tree_dir

    file_list = repo.git.status(porcelain = True)
    file_list = file_list.split('\n')
    file_list = [f.lstrip().lstrip('MADRCU?!').lstrip() for f in file_list]
    file_list = [root + "/" + f for f in file_list]
    file_list = [norm_path(f) for f in file_list]

    return(file_list)

def get_modified_sources(paths, 
                         move_map, 
                         recursive = float('inf')):
    """ Get source files considered changed by git status.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    move_map : list 
        Mapping of symlinks/copies (destination) to sources (returned from `MoveList.create_symlinks` or `MoveList.create_copies`).
    recursive : int, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Returns
    -------
    overlap : list
        List of source files considered changed by git status.
    """
    
    try:
        source_list = [source for source, destination in move_map]
        source_list = [glob_recursive(source, recursive) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)
   
        try:
            repo = git.Repo('.', search_parent_directories = True)    
        except:
            raise CritError(messages.crit_error_no_repo)
        modified = get_git_status(repo)

        overlap = [l for l in source_files if l in modified] 
			
        if overlap:
            if len(overlap) > 100:
                overlap = overlap[0:100]
                overlap = overlap + ["and more (file list truncated due to length)"]
            message = format_error(messages.warning_modified_files % '\n'.join(overlap))
            write_to_makelog(paths, message)
            print(message)
    except:
        error_message = 'Error with `get_modified_sources`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise