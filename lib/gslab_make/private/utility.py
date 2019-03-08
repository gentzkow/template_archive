#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import glob

import gslab_make.private.messages as messages


def norm_path(path):
    """ Normalizes path to be OS-compatible. """

    if path:
        path = re.split('[/\\\\]+', path)
        path = os.path.sep.join(path)
        path = path.rstrip(os.path.sep)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

    return path


def glob_recursive(path, recursive):
    """ Walks through path. 
    
    Notes
    -----
    Takes glob-style wildcards.

    Parameters
    ----------
    path : str
        Path to walk through.
    recursive : int
        Level of depth when walking through path.

    Returns
    -------
    path_files : list
        List of files contained in path.
    """

    path_walk = norm_path(path)
    path_files = glob.glob(path_walk)

    i = 0 
    while i <= recursive:          
        path_walk = os.path.join(path_walk, "*")
        glob_files = glob.glob(path_walk)
        if glob_files:
            path_files.extend(glob_files) 
            i += 1
        else:
            break

    path_files = [p for p in path_files if os.path.isfile(p)]
    if not path_files:
        print(messages.warning_glob % (path, recursive))

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


def format_error(error):
    """ Format error message. 

    Parameters
    ----------
    error : str
        Error message to format.

    Returns
    -------
    formatted : str
        Formatted error message.
    """

    formatted = messages.note_star_line + '\n%s\n' + messages.note_star_line
    formatted = formatted % error.strip()
    
    return(formatted)


def format_list(list):
    """ Format list. 

    Parameters
    ----------
    list : list
        List to format.

    Notes
    -----
    Format list for readability to pass into user messages 

    Returns
    -------
    formatted : str
        Formatted list.
    """

    formatted = ['`' + item + '`' for item in list]
    formatted = ", ".join(formatted)
    
    return(formatted)