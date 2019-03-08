#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from gslab_make.private.utility import norm_path, glob_recursive, format_error
from gslab_make.write_logs import write_to_makelog, write_stats_log, write_heads_log


def write_link_logs(paths, 
                    link_map,
                    recursive = float('inf')):        
    """ Write link logs.

    Notes
    -----
    The following information is logged:
        * Mapping of symlinks to targets (link map log)
        * Details on files contained in targets: 
            * File name (link statistics log)
            * Last modified (link statistics log)
            * File size (link statistics log)
            * File head (link headers log)
        * When walking through target directories, recursive determines depth.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'link_statslog' : str
                Path to write link statistics log.
            'link_headslog' : str
                Path to write link headers log.
            'link_maplog' : str
                Path to write link map log.
            'makelog' : str
                Path of makelog.
        }
    link_map : list 
        Mapping of symlinks to targets (returned from `LinksList.create_symlinks`).
    recursive : int, optional
        Level of depth when walking through target directories. Defaults to infinite.

    Returns
    -------
    None
    """

    link_statslog = paths['link_statslog']
    link_headslog = paths['link_headslog']
    link_maplog   = paths['link_maplog']

    try:
        target_list = [target for target, symlink in link_map]
        target_list = [glob_recursive(target, recursive) for target in target_list]
        target_files = [f for target in target_list for f in target]
        target_files = set(target_files)

        if link_statslog:
            link_statslog = norm_path(link_statslog)
            write_stats_log(link_statslog, target_files)

        if link_headslog:
            link_headslog = norm_path(link_headslog)
            write_heads_log(link_headslog, target_files)   

        if link_maplog:
            link_maplog = norm_path(link_maplog)
            write_link_maplog(link_maplog, link_map)

        write_to_makelog(paths, 'Link logs successfully written!')  
    except:
        error_message = 'Error with `write_link_logs`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise


def write_link_maplog(link_maplog, link_map):
    """ Write link map log.

    Parameters
    ----------
    link_maplog : str
        Path to write link map log.
    link_map : list 
        Mapping of symlinks to targets (returned by LinksList).

    Returns
    -------
    None
    """
    
    header = 'symlink\ttarget'

    with open(link_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for target, symlink in link_map:
            symlink = os.path.relpath(symlink)
            print("%s\t%s" % (symlink, target), file = MAPLOG)