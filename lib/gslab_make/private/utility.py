#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import glob
import traceback
import filecmp

import gslab_make.private.messages as messages
from gslab_make.private.exceptionclasses import CritError


def norm_path(path):
    """ Normalizes path to be OS-compatible. """

    if path:
        path = re.split('[/\\\\]+', path)
        path = os.path.sep.join(path)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

    return path


def get_path(paths_dict, key):
    """ Get path for key. """

    try:
        path = paths_dict[key]
    except KeyError:
        raise_from(CritError(messages.crit_error_no_key % (key, key)), None)

    return(path)


def glob_recursive(path, depth, quiet = True):
    """ Walks through path. 
    
    Notes
    -----
    Takes glob-style wildcards.

    Parameters
    ----------
    path : str
        Path to walk through.
    depth : int
        Level of depth when walking through path.
    quiet : bool, optional
        Suppress warning if no files globbed. Defaults to True. 

    Returns
    -------
    path_files : list
        List of files contained in path.
    """

    path_walk = norm_path(path)
    path_files = glob.glob(path_walk)

    i = 0 
    while i <= depth:          
        path_walk = os.path.join(path_walk, "*")
        glob_files = glob.glob(path_walk)
        if glob_files:
            path_files.extend(glob_files) 
            i += 1
        else:
            break

    path_files = [p for p in path_files if os.path.isfile(p)]
    
    if not path_files and not quiet:
        print(messages.warning_glob % (path, depth))

    return path_files

 
def file_to_array(file_name):
    """ Read file and extract lines to list. 

    Parameters
    ----------
    file_name : str
        Path of file to read.

    Returns
    -------
    array : list
        List of lines contained in file.
    """
       
    with open(file_name, 'r') as f:
        array = [line.strip() for line in f]
        array = [line for line in array if line]
        array = [line for line in array if not re.match('\#',line)]

    return array


def format_traceback(trace = ''):
    """ Format traceback message.

    Parameters
    ----------
    trace : str
        Traceback to format. Defaults to `traceback.format_exc()`.

    Notes
    -----
    Format trackback for readability to pass into user messages. 

    Returns
    -------
    formatted : str
        Formatted traceback.
    """
    
    if not trace:
        trace = traceback.format_exc()

    trace = '\n' + trace.strip()
    formatted = re.sub('\n', '\n  > ', trace)

    return(formatted)


def format_message(message):
    """ Format message. """

    message = message.strip()
    star_line = '*' * (len(message) + 4)
    formatted = star_line + '\n* %s *\n' + star_line
    formatted = formatted % message

    return(formatted)


def format_list(list):
    """ Format list. 

    Parameters
    ----------
    list : list
        List to format.

    Notes
    -----
    Format list for readability to pass into user messages.

    Returns
    -------
    formatted : str
        Formatted list.
    """

    formatted = ['`' + str(item) + '`' for item in list]
    formatted = ", ".join(formatted)
    
    return(formatted)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Following functions are not currently actively used in code base #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def check_duplicate(original, copy): 
    """ Check duplicate.

    Parameters
    ----------
    original : str
        Original path.
    copy : str 
        Path to check if duplicate.

    Returns
    -------
    duplicate : bool
        Destination is duplicate.
    """

    duplicate = os.path.exists(copy)
    
    if duplicate: 
        if os.path.isfile(original):
            duplicate = filecmp.cmp(original, copy)            
        elif os.path.isdir(copy):
            dircmp = filecmp.dircmp(original, copy, ignore = ['.DS_Store'])
            duplicate = parse_dircmp(dircmp)
        else:
            duplicate = False
            
    return duplicate
    

def parse_dircmp(dircmp):
    """ Parse dircmp to see if directories duplicate. 

    Parameters
    ----------
    dircmp : filecmp.dircmp
        dircmp to parse if directories duplicate.

    Returns
    -------
    duplicate : bool
        Directories are duplicates.
    """

    # Check directory
    if dircmp.left_only:
        return False
    if dircmp.right_only:
        return False
    if dircmp.diff_files:
        return False
    if dircmp.funny_files:
        return False
    if dircmp.common_funny:
        return False

    # Check subdirectories
    duplicate = True
    
    for subdir in dircmp.subdirs.itervalues():
        if duplicate:
            duplicate = check_duplicate(subdir)
        else:
            break
        
    return duplicate