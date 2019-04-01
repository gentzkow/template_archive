#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from gslab_make.private.utility import norm_path, glob_recursive, format_error
from gslab_make.write_logs import write_to_makelog, write_stats_log, write_heads_log


def write_source_logs(paths, 
                      source_map,
                      recursive = float('inf')):        
    """ Write source logs.

    Notes
    -----
    The following information is logged:
        * Mapping of symlinks/copies to sources (source map log)
        * Details on files contained in sources: 
            * File name (source statistics log)
            * Last modified (source statistics log)
            * File size (source statistics log)
            * File head (source headers log)
        * When walking through source directories, recursive determines depth.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'source_statslog' : str
                Path to write source statistics log.
            'source_headslog' : str
                Path to write source headers log.
            'source_maplog' : str
                Path to write source map log.
            'makelog' : str
                Path of makelog.
        }
    source_map : list 
        Mapping of symlinks/copies (destination) to sources (returned from `MoveList.create_symlinks` or `MoveList.create_copies`).
    recursive : int, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Returns
    -------
    None
    """

    source_statslog = paths['source_statslog']
    source_headslog = paths['source_headslog']
    source_maplog   = paths['source_maplog']

    try:
        source_list = [source for source, destination in source_map]
        source_list = [glob_recursive(source, recursive) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)

        if source_statslog:
            source_statslog = norm_path(source_statslog)
            write_stats_log(source_statslog, source_files)

        if source_headslog:
            source_headslog = norm_path(source_headslog)
            write_heads_log(source_headslog, source_files)   

        if source_maplog:
            source_maplog = norm_path(source_maplog)
            write_source_maplog(source_maplog, source_map)

        write_to_makelog(paths, 'Source logs successfully written!')  
    except:
        error_message = 'Error with `write_source_logs`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise


def write_source_maplog(source_maplog, source_map):
    """ Write link map log.

    Parameters
    ----------
    source_maplog : str
        Path to write link map log.
    source_map : list 
        Mapping of symlinks to sources (returned by LinksList).

    Returns
    -------
    None
    """
    
    header = 'destination\tsource'

    with open(source_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for source, destination in source_map:
            destination = os.path.relpath(destination)
            print("%s\t%s" % (destination, source), file = MAPLOG)