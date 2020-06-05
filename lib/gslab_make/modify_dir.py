# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import sys
import glob
import zipfile
import traceback
import subprocess

if (sys.version_info < (3, 0)) and (os.name == 'nt'):
    import gslab_make.private.subprocess_fix as subprocess_fix
else:
    import subprocess as subprocess_fix

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata
import gslab_make.private.messages as messages
from gslab_make.private.exceptionclasses import ColoredError
from gslab_make.private.utility import convert_to_list, norm_path, format_message


def remove_path(path, option = '', quiet = False):
    """.. Remove path using system command.
    
    Remove path ``path`` using system command. Safely removes symbolic links. 
    Path can be specified with the * shell pattern 
    (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__).

    Parameters
    ----------
    path : str
        Path to remove.
    option : str, optional
        Options for system command. Defaults to ``-rf`` for POSIX and ``/s /q`` for NT.
    quiet : bool, optional
        Suppress printing of path removed. Defaults to ``False``. 

    Returns
    -------
    None

    Example
    -------
    The following code removes path ``path``.

    .. code-block:: python

        remove_path('path')

    The following code removes all paths beginning with ``path``.

    .. code-block:: python
    
        remove_path('path*')
    """

    try:
        path = norm_path(path)
        if not option:
            option = metadata.default_options[os.name]['rmdir']

        command = metadata.commands[os.name]['rmdir'] % (option, path)
        process = subprocess_fix.Popen(command, shell = True)   
        process.wait()
        # ACTION ITEM: ADD DEBUGGING TO SUBPROCESS CALL

        if not quiet:
            message = 'Removed: `%s`' % path
            print(colored(message, metadata.color_success))
    except:
        error_message = 'Error with `remove_path`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def remove_dir(dir_list, quiet = False):
    """.. Remove directory using system command.
    
    Remove directories in list ``dir_list`` using system command. 
    Safely removes symbolic links. Directories can be specified with the * shell pattern 
    (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__).

    Parameters
    ----------
    dir_list : str, list
        Directory or list of directories to remove.
    quiet : bool, optional
        Suppress printing of directories removed. Defaults to ``False``. 

    Returns
    -------
    None

    Example
    -------
    The following code removes directories ``dir1`` and ``dir2``.

    .. code-block:: python

        remove_dir(['dir1', 'dir2'])

    The following code removes directories beginning with ``dir``.

    .. code-block:: python

        remove_dir(['dir1*'])
    """
    
    try:
        dir_list = convert_to_list(dir_list, 'dir')
        dir_list = [norm_path(dir_path) for dir_path in dir_list]
        dir_list = [d for directory in dir_list for d in glob.glob(directory)]

        for dir_path in dir_list:
            if os.path.isdir(dir_path):
                remove_path(dir_path, quiet = quiet)
            elif os.path.isfile(dir_path): 
                raise_from(TypeError(messages.type_error_not_dir % dir_path), None)
    except:
        error_message = 'Error with `remove_dir`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def clear_dir(dir_list):
    """.. Clear directory. Create directory if nonexistent.
    
    Clears all directories in list ``dir_list`` using system command. 
    Safely clears symbolic links. Directories can be specified with the * shell pattern 
    (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__).

    Note
    ----
    To clear a directory means to remove all contents of a directory. 
    If the directory is nonexistent, the directory is created, 
    unless the directory is specified via shell pattern.

    Parameters
    ----------
    dir_list : str, list
        Directory or list of directories to clear.

    Returns
    -------
    None

    Example
    -------
    The following code clears directories ``dir1`` and ``dir2``.

    .. code-block:: python

        clear_dir(['dir1', 'dir2'])

    The following code clears directories beginning with ``dir``.

    .. code-block:: python

        clear_dir(['dir*'])
    """

    try:
        dir_list = convert_to_list(dir_list, 'dir')
        dir_glob = []
        
        for dir_path in dir_list:
            expand = glob.glob(dir_path)
            expand = expand if expand else [dir_path]
            dir_glob.extend(expand)

        remove_dir(dir_glob, quiet = True)

        for dir_path in dir_glob:
            os.makedirs(dir_path)
            message = 'Cleared: `%s`' % dir_path
            print(colored(message, metadata.color_success))
    except:
        error_message = 'Error with `clear_dir`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def unzip(zip_path, output_dir):
    """.. Unzip file to directory.

    Unzips file ``zip_path`` to directory ``output_dir``.

    Parameters
    ----------
    zip_path : str
        Path of file to unzip.
    output_dir : str
        Directory to write outputs of unzipped file.

    Returns
    -------
    None
    """

    try:
        with zipfile.ZipFile(zip_path, allowZip64 = True) as z:
            z.extractall(output_dir)
    except:
        error_message = 'Error with `zip_path`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def zip_dir(source_dir, zip_dest):
    """.. Zip directory to file.

    Zips directory ``source_dir`` to file ``zip_dest``.

    Parameters
    ----------
    source_dir : str
        Path of directory to zip.
    zip_dest : str
        Destination of zip file.

    Returns
    -------
    None
    """

    try:
        with zipfile.ZipFile('%s' % (zip_dest), 'w', zipfile.ZIP_DEFLATED, allowZip64 = True) as z:
            source_dir = norm_path(source_dir)

            for root, dirs, files in os.walk(source_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    file_name = os.path.basename(file_path)
                    z.write(file_path, file_name)
                    
                    message = 'Zipped: `%s` as `%s`' % (file_path, file_name)
                    print(colored(message, metadata.color_success))
    except:
        error_message = 'Error with `zip_dir`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


__all__ = ['remove_dir', 'clear_dir', 'unzip', 'zip_dir']