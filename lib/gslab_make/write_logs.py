# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import io
import datetime
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import convert_to_list, norm_path, get_path, glob_recursive, format_message


def start_makelog(paths):
    """.. Start make log.

    Writes file ``makelog``, recording start time. 
    Sets make log status to boolean ``True``, which is used by other functions to confirm make log exists.

    Note
    ----
    The make log start condition is used by other functions to confirm a make log exists.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        metadata.makelog_started = True
        
        if makelog:
            makelog = norm_path(makelog)
            message = 'Starting makelog file at: `%s`' % makelog
            print(colored(message, metadata.color_success))
            
            with io.open(makelog, 'w', encoding = 'utf8', errors = 'ignore') as MAKELOG:
                time_start = str(datetime.datetime.now().replace(microsecond = 0))
                working_dir = os.getcwd()
                print(messages.note_dash_line, file = MAKELOG)
                print(messages.note_makelog_start + time_start, file = MAKELOG)
                print(messages.note_working_directory + working_dir, file = MAKELOG)
                print(messages.note_dash_line, file = MAKELOG)
    except:
        error_message = 'Error with `start_makelog`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def end_makelog(paths):
    """.. End make log.

    Appends to file ``makelog``, recording end time.

    Note
    ----
    We technically allow for writing to a make log even after the make log has ended. 
    We do not recommend this for best practice.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Returns
    -------
    None
    """
 
    try:
        makelog = get_path(paths, 'makelog')

        if makelog:
            makelog = norm_path(makelog)
            message = 'Ending makelog file at: `%s`' % makelog
            print(colored(message, metadata.color_success))

            if not (metadata.makelog_started and os.path.isfile(makelog)):
                raise_from(CritError(messages.crit_error_no_makelog % makelog), None)

            with io.open(makelog, 'a', encoding = 'utf8', errors = 'ignore') as MAKELOG:
                time_end = str(datetime.datetime.now().replace(microsecond = 0))
                working_dir = os.getcwd()
                print(messages.note_dash_line, file = MAKELOG)
                print(messages.note_makelog_end + time_end, file = MAKELOG)
                print(messages.note_working_directory + working_dir, file = MAKELOG)
                print(messages.note_dash_line, file = MAKELOG)
    except:
        error_message = 'Error with `end_makelog`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
    

def write_to_makelog(paths, message):
    """.. Write to make log.

    Appends string ``message`` to file ``makelog``.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    message : str
        Message to append.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Returns
    -------
    None
    """

    makelog = get_path(paths, 'makelog')

    if makelog:
        makelog = norm_path(makelog)

        if not (metadata.makelog_started and os.path.isfile(makelog)):
            raise_from(CritError(messages.crit_error_no_makelog % makelog), None)

        with io.open(makelog, 'a', encoding = 'utf8', errors = 'ignore') as MAKELOG:
            print(message, file = MAKELOG)
    
    
def log_files_in_output(paths,
                        depth = float('inf')):
    """.. Log files in output directory.

    Logs the following information for all files contained in directory ``output_dir``.

    - File name (in file ``output_statslog``)
    - Last modified (in file ``output_statslog``)
    - File size (in file ``output_statslog``)
    - File head (in file ``output_headslog``, optional)

    When walking through directory ``output_dir``, float ``depth`` determines level of depth to walk. 
    Status messages are appended to file ``makelog``. 

    Include additional output directories to walk through 
    (typically directories that you wish to keep local) in directory list ``output_local_dir``. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    depth : float, optional
        Level of depth when walking through output directory. Defaults to infinite.

    Path Keys
    ---------
    output_dir : str
       Path of output directory.
    output_local_dir : str, list, optional
       Path or list of paths of local output directories. Defaults to ``[]`` (i.e., none).
    output_statslog : str
       Path to write output statistics log.
    output_headslog : str, optional
       Path to write output headers log.
    makelog : str
       Path of makelog.

    Returns
    -------
    None

    Example
    -------
    The following code will log information for all files contained in 
    only the first level of ``paths['output_dir']``. 
    Therefore, files contained in subdirectories will be ignored.
    
    .. code-block:: python

        log_files_in_outputs(paths, depth = 1)

    The following code will log information for any file in ``paths['output_dir']``, 
    regardless of level of subdirectory.
    
    .. code-block :: python

        log_files_in_outputs(paths, depth = float('inf'))
    """
    
    try:
        output_dir      =  get_path(paths, 'output_dir')
        output_local_dir = get_path(paths, 'output_local_dir', throw_error = False) 
        output_statslog  = get_path(paths, 'output_statslog')
        output_headslog  = get_path(paths, 'output_headslog', throw_error = False)
        
        if output_local_dir:
            output_local_dir = convert_to_list(output_local_dir, 'dir') 
        else:
            output_local_dir = []

        output_files = glob_recursive(output_dir, depth)
        output_local_files = [f for dir_path in output_local_dir for f in glob_recursive(dir_path, depth)]   
        output_files = set(output_files + output_local_files)

        if output_statslog:
            output_statslog = norm_path(output_statslog)
            _write_stats_log(output_statslog, output_files)
        
        if output_headslog:
            output_headslog = norm_path(output_headslog)
            _write_heads_log(output_headslog, output_files)
        
        message = 'Output logs successfully written!'
        write_to_makelog(paths, message)
        print(colored(message, metadata.color_success))  
    except:
        error_message = 'Error with `log_files_in_output`. Traceback can be found below.' 
        error_message = format_message(error_message)
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)

    
def _write_stats_log(statslog_file, output_files):
    """.. Write statistics log.

    Logs the following information to ``statslog_file`` for all files contained in list ``output_files``.
    
    - File name 
    - Last modified 
    - File size

    Parameters
    ----------
    statslog_file : str
        Path to write statistics log. 
    output_files : list
        List of output files to log statistics.

    Returns
    -------
    None
    """

    header = "file name | last modified | file size"
    
    with io.open(statslog_file, 'w', encoding = 'utf8', errors = 'ignore') as STATSLOG:
        print(header, file = STATSLOG)      

        for file_name in output_files:
            stats = os.stat(file_name)
            last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
            file_size = stats.st_size

            print("%s | %s | %s" % (file_name, last_mod, file_size), file = STATSLOG)


# ~~~~~~~~~~ #
# DEPRECATED #
# ~~~~~~~~~~ #

def _write_heads_log(headslog_file, output_files, num_lines = 10):
    """.. Write headers log.

    Logs the following information to ``headslog_file`` for all files contained in file list ``output_files``:
    
    Parameters
    ----------
    headslog_file : str
        Path to write headers log. 
    output_files list
        List of output files to log headers.
    num_lines: ``int``, optional
        Number of lines for headers. Default is ``10``.

    Returns
    -------
    None
    """

    header = "File headers"

    with io.open(headslog_file, 'w', encoding = 'utf8', errors = 'ignore') as HEADSLOG:      
        print(header, file = HEADSLOG)
        print(messages.note_dash_line, file = HEADSLOG)
        
        for file_name in output_files:
            print("%s" % file_name, file = HEADSLOG)
            print(messages.note_dash_line, file = HEADSLOG)
            
            try:
                with io.open(file_name, 'r', encoding = 'utf8', errors = 'ignore') as f:
                    for i in range(num_lines):
                        line = f.readline().rstrip('\n')
                        print(line, file = HEADSLOG)
            except:
                print("Head not readable or less than %s lines" % num_lines, file = HEADSLOG)
            print(messages.note_dash_line, file = HEADSLOG)


__all__ = ['start_makelog', 'end_makelog', 'write_to_makelog', 'log_files_in_output']