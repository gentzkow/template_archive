#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from gslab_make.private.linkdirective import LinksList
from gslab_make.private.utility import format_error
from gslab_make.write_logs import write_to_makelog


def create_links(paths,
                 file_list,
                 file_format, 
                 mapping_dict = {}):
    """ Create symlinks from list of files containing linking instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'link_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    file_format : str
        Format of files from which to parse linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    link_map : list
        List of (target, symlink) for each symlink created.
    """

    link_dir = paths['link_dir']

    try:              
        link_list = LinksList(file_list, file_format, link_dir, mapping_dict)
        if link_list.link_directive_list:
            os.makedirs(link_dir)
            link_map = link_list.create_symlinks()       
        else:
            link_map = []

        write_to_makelog(paths, 'Links successfully created!')    
        return(link_map)
    except:
        error_message = 'An error was encountered with `create_links`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise               


def create_input_links(paths,
                       file_list,
                       mapping_dict = {}):
    """ 
    Create symlinks from list of files containing linking instructions. 

    Notes
    -----
    Linking instructions should be in input format.

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
    link_map : list
        List of (target, symlink) for each symlink created.
    """
    paths['link_dir'] = paths['input_dir']
    link_map = create_links(paths, file_list, "input", mapping_dict)
    return(link_map)


def create_external_links(paths,
                          file_list,
                          mapping_dict = {}):
    """ 
    Create symlinks from list of files containing linking instructions. 

    Notes
    -----
    Linking instructions should be in external format.

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
    link_map : list
        List of (target, symlink) for each symlink created.
    """
    paths['link_dir'] = paths['external_dir']
    link_map = create_links(paths, file_list, "external", mapping_dict)
    return(link_map)