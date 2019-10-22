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
from gslab_make.private.utility import norm_path, get_path, glob_recursive, format_message
from gslab_make.write_logs import write_to_makelog, _write_stats_log, _write_heads_log


def write_source_logs(paths, 
                      source_map,
                      depth = float('inf')):        
    """.. Write source logs.

    Logs the following information for sources contained in list ``source_map`` 
    (returned by `sourcing functions`_).
    
    - Mapping of symlinks/copies to sources (in file ``source_maplog``)
    - Details on files contained in sources: 

        - File name (in file ``source_statslog``)
        - Last modified (in file ``source_statslog``)
        - File size (in file ``source_statslog``)
        - File head (in file ``source_headlog``, optional)

    When walking through sources, float ``depth`` determines level of depth to walk. 
    Status messages are appended to file ``makelog``. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    source_map : list
        Mapping of symlinks/copies (destination) to sources (returned by `sourcing functions`_).
    depth : float, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Path Keys
    ---------
    source_statslog : str
       Path to write source statistics log.
    source_headslog : str, optional
       Path to write source headers log.
    source_maplog : str
       Path to write source map log.
    makelog : str
       Path of makelog.

    Returns
    -------
    None

    Example
    -------
    The following code will log information for all files listed in ``source_map``. 
    Therefore, files contained in directories listed in ``source_map`` will be ignored.
    
    .. code-block:: python

        write_source_logs(paths, depth = 1)

    The following code will log information for all files listed in ``source_map`` 
    and any file in all directories listed in ``source_map``, regardless of level of subdirectory.
    
    .. code-block :: python

        write_source_logs(paths, depth = float('inf'))
    """

    try:
        source_statslog = get_path(paths, 'source_statslog')
        source_headslog = get_path(paths, 'source_headslog', throw_error = False)
        source_maplog   = get_path(paths, 'source_maplog')

        source_list = [source for source, destination in source_map]
        source_list = [glob_recursive(source, depth) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)

        # ACTION: DECIDE WHETHER TO ALLOW FOR RAW DIRECTORY
        raw_dir = get_path(paths, 'raw_dir', throw_error = False)
        if raw_dir:
            raw_files = glob_recursive(raw_dir)
            source_files = set(source_files + raw_files)

        if source_statslog:
            source_statslog = norm_path(source_statslog)
            _write_stats_log(source_statslog, source_files)

        if source_headslog:
            source_headslog = norm_path(source_headslog)
            _write_heads_log(source_headslog, source_files)   

        if source_maplog:
            source_maplog = norm_path(source_maplog)
            _write_source_maplog(source_maplog, source_map)

        message = 'Source logs successfully written!'
        write_to_makelog(paths, message)  
        print(colored(message, metadata.color_success))
    except:
        error_message = 'Error with `write_source_logs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def _write_source_maplog(source_maplog, source_map):
    """.. Write link map log.

    Parameters
    ----------
    source_maplog : str
        Path to write link map log.
    source_map : list 
        Mapping of symlinks to sources (returned by `sourcing functions`_).

    Returns
    -------
    None
    """
    
    header = 'destination | source'

    with open(source_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for source, destination in source_map:
            destination = os.path.relpath(destination)
            print("%s | %s" % (destination, source), file = MAPLOG)