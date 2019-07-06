#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import git
import fnmatch
import yaml
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import norm_path, get_path, format_error, glob_recursive
from gslab_make.write_logs import write_to_makelog


def check_os(osname = os.name):
    """ Check OS is either POSIX or NT. 
    
    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.

    Returns
    -------
    None
    """

    if (osname != 'posix') & (osname != 'nt'):
        raise CritError(messages.crit_error_unknown_system % osname)


def update_executables(paths, osname = os.name):
    """ Update executable names using user config file. 
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'config_user' : str
                Path of user config file.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.

    Returns
    -------
    None
    """

    config_user = get_path(paths, 'config_user')
    config_user = yaml.load(open(config_user, 'rb'))
    
    check_os(osname)
    
    if config_user['local']['executables']:
        metadata.default_executables[osname].update(config_user['local']['executables'])


def update_mappings(paths, mapping_dict = {}):
    """ Update path mappings using user config file. 
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'config_user' : str
                Path of user config file.
        }
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse paths. 
        Defaults to no mappings.

    Returns
    -------
    mapping_dict : dict
        Dictionary of path mappings used to parse paths. 
    """

    config_user = get_path(paths, 'config_user')
    config_user = yaml.load(open(config_user, 'rb'))

    if config_user['external']:
        mapping_dict.update(config_user['external'])

    return(mapping_dict)

