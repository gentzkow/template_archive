# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import shutil
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import get_path, format_message, norm_path, open_yaml


def _check_os(osname = os.name):
    """Check OS is either POSIX or NT. 
    
    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to ``os.name``.

    Returns
    -------
    None
    """

    if osname not in ['posix', 'nt']:
        raise CritError(messages.crit_error_unknown_system % osname)


def update_executables(paths, osname = None):
    """.. Update executable names using user configuration file. 
    
    Updates executable names with executables listed in file ``config_user``.
    
    Note
    ----
    Executable names are used by :ref:`program functions <program functions>`.
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    osname : str, optional
        Name of OS. Defaults to ``os.name``.

    Path Keys
    ---------
    config_user : str
        Path of user configuration file.   

    Returns
    -------
    None
    """

    osname = osname if osname else os.name # https://github.com/sphinx-doc/sphinx/issues/759

    try:
        config_user = get_path(paths, 'config_user')
        config_user = open_yaml(config_user)
    
        _check_os(osname)
    
        if config_user['local']['executables']:
            metadata.default_executables[osname].update(config_user['local']['executables'])
    except:
        error_message = 'Error with update_executables. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def update_paths(paths):
    """.. Update paths using user configuration file. 
    
    Updates dictionary ``paths`` with externals listed in file ``config_user``.
    
    Note
    ----
    The ``paths`` argument for :ref:`sourcing functions<sourcing functions>` is used not only to get 
    default paths for writing/logging, but also to 
    `string format <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ 
    sourcing instructions.
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths to update. 
        Dictionary should ex-ante contain values for all keys listed below.

    Path Keys
    ---------
    config_user : str
        Path of user configuration file.  

    Returns
    -------
    paths : dict
        Dictionary of updated paths. 
    """

    try:
        config_user = get_path(paths, 'config_user')
        config_user = open_yaml(config_user)

        if config_user['external']:
            paths.update(config_user['external'])

        return(paths)
    except:
        error_message = 'Error with update_paths. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_output(file, copy_dir):
    """.. Copy output file.
    
    Copies output ``file`` to directory ``copy_dir`` with user prompt to confirm copy.
    
    Parameters
    ----------
    file : str
        Path of file to copy.
    copy_dir : str
        Directory to copy file.

    Returns
    -------
    None
    """

    file = norm_path(file)
    copy_dir = norm_path(copy_dir)
    message = colored(messages.warning_copy, color = 'cyan')
    upload = input(message % (file, copy_dir))

    if upload.lower().strip() == "yes":
        shutil.copy(file, copy_dir)


__all__ = ['update_executables', 'update_paths', 'copy_output']
