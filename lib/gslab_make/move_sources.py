#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import ColoredError
from gslab_make.private.movedirective import MoveList
from gslab_make.private.utility import get_path, format_message
from gslab_make.write_logs import write_to_makelog


def create_links(paths,
                 file_list,
                 mapping_dict = {}):
    """ Create symlinks from list of files containing linking instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'move_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """
             
    move_dir = get_path(paths, 'move_dir')

    move_list = MoveList(file_list, move_dir, mapping_dict)
    if move_list.move_directive_list:
        os.makedirs(move_dir)
        move_map = move_list.create_symlinks()       
    else:
        move_map = []

    return(move_map)
        

def create_copies(paths,
                  file_list,
                  mapping_dict = {}):
    """ Create copies from list of files containing copying instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'move_dir' : str
                Directory to write copies.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing copying instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse copying instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each copy created.
    """
             
    move_dir = get_path(paths, 'move_dir')

    move_list = MoveList(file_list, move_dir, mapping_dict)
    if move_list.move_directive_list:
        os.makedirs(move_dir)
        move_map = move_list.create_copies()       
    else:
        move_map = []

    return(move_map)


def link_inputs(paths,
                file_list,
                mapping_dict = {}):
    """ 
    Create symlinks to inputs from list of files containing linking instructions. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'input_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """
    
    try:
        paths['move_dir'] = get_path(paths, 'input_dir')
        move_map = create_links(paths, file_list, mapping_dict)

        message = 'Input links successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))
        return(move_map)
    except:
        error_message = 'An error was encountered with `link_inputs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def link_externals(paths,
                   file_list,
                   mapping_dict = {}):
    """ 
    Create symlinks to externals from list of files containing linking instructions. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'external_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """
    
    try:
        paths['move_dir'] = get_path(paths, 'external_dir')
        move_map = create_links(paths, file_list, mapping_dict)

        message = 'External links successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))
        return(move_map)
    except:
        error_message = 'An error was encountered with `link_externals`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_inputs(paths,
                file_list,
                mapping_dict = {}):
    """ Create copies to inputs from list of files containing copying instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'input_dir' : str
                Directory to write copies.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing copying instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse copying instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each copy created.
    """
        
    try:
        paths['move_dir'] = get_path(paths, 'input_dir')
        move_map = create_copies(paths, file_list, mapping_dict)

        message = 'Input copies successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))
        return(move_map)
    except:
        error_message = 'An error was encountered with `copy_inputs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_externals(paths,
                file_list,
                mapping_dict = {}):
    """ Create copies to externals from list of files containing copying instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'external_dir' : str
                Directory to write copies.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing copying instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse copying instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each copy created.
    """
        
    try:
        paths['move_dir'] = get_path(paths, 'external_dir')
        move_map = create_copies(paths, file_list, mapping_dict)

        message = 'External copies successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))
        return(move_map)
    except:
        error_message = 'An error was encountered with `copy_externals`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)