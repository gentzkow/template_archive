#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import datetime
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import norm_path, get_path, glob_recursive, format_error


def start_makelog(paths):
    """ Start make log. Record start time.

    Notes
    -----
    The make log start condition is needed by other functions to confirm a 
    make log exists.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }

    Returns
    -------
    None
    """

    makelog = get_path(paths, 'makelog')

    metadata.makelog_started = True
    
    if makelog:
        makelog = norm_path(makelog)
        message = 'Starting makelog file at: `%s`' % makelog
        print(colored(message, 'green'))
        
        with open(makelog, 'w', encoding = 'utf8') as MAKELOG:
            time_start = str(datetime.datetime.now().replace(microsecond = 0))
            working_dir = os.getcwd()
            print(messages.note_dash_line, file = MAKELOG)
            print(messages.note_makelog_start + time_start, file = MAKELOG)
            print(messages.note_working_directory + working_dir, file = MAKELOG)
            print(messages.note_dash_line, file = MAKELOG)


def end_makelog(paths):
    """ End make log. Record end time.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }

    Returns
    -------
    None
    """
 
    makelog = get_path(paths, 'makelog')

    if makelog:
        makelog = norm_path(makelog)
        message = 'Ending makelog file at: `%s`' % makelog
        print(colored(message, 'green'))

        if not (metadata.makelog_started and os.path.isfile(makelog)):
            raise CritError(messages.crit_error_no_makelog % makelog)

        with open(makelog, 'a', encoding = 'utf8') as MAKELOG:
            time_end = str(datetime.datetime.now().replace(microsecond = 0))
            working_dir = os.getcwd()
            print(messages.note_dash_line, file = MAKELOG)
            print(messages.note_makelog_end + time_end, file = MAKELOG)
            print(messages.note_working_directory + working_dir, file = MAKELOG)
            print(messages.note_dash_line, file = MAKELOG)

    metadata.makelog_started = False
    
    
def write_to_makelog(paths, message):
    """ Append message to make log.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    message : str
        Message to append.

    Returns
    -------
    None
    """

    makelog = get_path(paths, 'makelog')

    if makelog:
        makelog = norm_path(makelog)

        if not (metadata.makelog_started and os.path.isfile(makelog)):
            raise CritError(messages.crit_error_no_makelog % makelog)

        with open(makelog, 'a', encoding = 'utf8') as MAKELOG:
            print(message, file = MAKELOG)
    
    
def log_files_in_output(paths,
                        depth = float('inf')):
    """ Log files in output directory.

    Notes
    -----
    The following information is logged of all files contained in output directory:
        * File name (output statistics log)
        * Last modified (output statistics log)
        * File size (output statistics log)
        * File head (output headers log)
    * When walking through output directory, depth determines depth.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'output_dir' : str
                Path of output directory.
            'output_local_dir' : list, optional
                List of paths of local output directories. Defaults to `[]`.
            'output_statslog' : str
                Path to write output statistics log.
            'output_headslog' : str
                Path to write output headers log.
            'makelog' : str
                Path of makelog.
        }
    depth : float, optional
        Level of depth when walking through output directory.

    Returns
    -------
    None
    """

    output_dir      = get_path(paths, 'output_dir')
    output_statslog = get_path(paths, 'output_statslog')
    output_headslog = get_path(paths, 'output_headslog')
    try:
        output_local_dir = get_path(paths, 'output_local_dir') # Make required?
        if type(output_local_dir) is not list:
            raise TypeError(messages.type_error_dir_list % output_local_dir)
    except KeyError:
        output_local_dir = []
  
    try:
        output_files = glob_recursive(output_dir, depth)
        output_local_files = [f for dir_path in output_local_dir for f in glob_recursive(dir_path, depth)]   
        output_files = set(output_files + output_local_files)

        if output_statslog:
            output_statslog = norm_path(output_statslog)
            write_stats_log(output_statslog, output_files)
        
        if output_headslog:
            output_headslog = norm_path(output_headslog)
            write_heads_log(output_headslog, output_files)
        
        message = 'Output logs successfully written!'
        write_to_makelog(paths, message)
        print(colored(message, 'green'))  
    except:
        error_message = 'Error with `log_files_in_output`. Traceback can be found below.' 
        error_message = format_error(error_message)
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())

    
def write_stats_log(statslog_file, output_files):
    """ Write statistics log.
   
    Notes
    -----
    The following information is logged of all output files:
        * File name 
        * Last modified 
        * File size

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
    
    with open(statslog_file, 'w', encoding = 'utf8') as STATSLOG:
        print(header, file = STATSLOG)      

        for file_name in output_files:
            stats = os.stat(file_name)
            last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
            file_size = stats.st_size

            print("%s | %s | %s" % (file_name, last_mod, file_size), file = STATSLOG)


def write_heads_log(headslog_file, output_files, num_lines = 10):
    """ Write headers log.

    Parameters
    ----------
    headslog_file : str
        Path to write headers log. 
    output_files : list
        List of output files to log headers.
    num_lines: int, optional
        Number of lines for headers. Default is 10.

    Returns
    -------
    None
    """

    header = "File headers"

    with open(headslog_file, 'w', encoding = 'utf8') as HEADSLOG:      
        print(header, file = HEADSLOG)
        print(messages.note_dash_line, file = HEADSLOG)
        
        for file_name in output_files:
            print("%s" % file_name, file = HEADSLOG)
            print(messages.note_dash_line, file = HEADSLOG)
            
            try:
                with open(file_name, 'r', encoding = 'utf8') as f:
                    for i in range(num_lines):
                        line = f.readline().rstrip('\n')
                        print(line, file = HEADSLOG)
            except:
                print("Head not readable or less than %s lines" % num_lines, file = HEADSLOG)
            print(messages.note_dash_line, file = HEADSLOG)