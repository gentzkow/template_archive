# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import git
import fnmatch
import traceback
from datetime import datetime
import filecmp
import subprocess

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata
import gslab_make.private.messages as messages
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import norm_path, get_path, format_message, glob_recursive, open_yaml
from gslab_make.write_logs import write_to_makelog


def _get_file_sizes(dir_path, exclude):
    """.. Walk through directory and get file sizes.
    
    Get file sizes for files in directory ``dir_path``, ignoring subdirectories in list ``exclude``.

    Parameters
    ----------
    dir_path : str
       Path of directory to walk through.
    exclude : list
       List of subdirectories to exclude when walking.

    Returns
    -------
    file_size : dict
        Dictionary of ``{file : size}`` for each file in ``dir_path``. 
    """

    file_sizes = []
    
    for root, dirs, files in os.walk(dir_path, topdown = True):
        dirs[:] = [d for d in dirs if d not in exclude]
        
        files = [os.path.join(root, f) for f in files]
        files = [norm_path(f) for f in files]
        sizes = [os.lstat(f).st_size for f in files]
        file_sizes.extend(zip(files, sizes))
        
    file_sizes = dict(file_sizes)
    
    return(file_sizes)

     
def _get_git_ignore(repo):
    """.. Get files ignored by git.
    
    Get files ignored by git for repository ``repo``.

    Parameters
    ----------
    repo : :class:`git.Repo`
        Git repository to get ignored files.

    Returns
    -------
    ignore_files : list
        List of files in repository ignored by git. 
    """

    g = git.Git(repo)
    root = repo.working_tree_dir

    ignore = g.execute('git status --porcelain --ignored', shell = True).split('\n')
    ignore = [i for i in ignore if re.match('!!', i)]
    ignore = [i.lstrip('!!').strip() for i in ignore]
    ignore = [os.path.join(root, i) for i in ignore]

    ignore_files = []

    for i in ignore:
        if os.path.isfile(i):
            ignore_files.append(i)
        elif os.path.isdir(i):
            for root, dirs, files in os.walk(i):
                files = [os.path.join(root, f) for f in files]
                ignore_files.extend(files)

    ignore_files = [norm_path(i) for i in ignore_files]
    
    return(ignore_files)


def _parse_git_attributes(attributes):
    """.. Get git lfs patterns from git attributes.

    Get git lfs patterns from file ``attributes``.

    Parameters
    ----------
    attributes : str
        Path of git attributes file.

    Returns
    -------
    lfs_list: list
        List of patterns to determine files tracked by git lfs. 
    """

    try:
        with open(attributes) as f:
            attributes_list = f.readlines()
        
            lfs_regex = 'filter=lfs( )+diff=lfs( )+merge=lfs( )+-text'      
            lfs_list = [l for l in attributes_list if re.search(lfs_regex, l)]
            lfs_list = [l.split()[0] for l in lfs_list] 

            return(lfs_list)
    except IOError:
        raise_from(CritError(messages.crit_error_no_attributes), None)
    

def _check_path_lfs(path, lfs_list):
    """.. Check if file matches git lfs patterns."""

    for l in lfs_list:
        if fnmatch.fnmatch(path, l):
            return(True)
            
    return(False)


def _get_dir_sizes(dir_path):
    """.. Get file sizes for directory.
    
    Get file sizes for files in directory ``dir_path``.

    Parameters
    ----------
    dir_path : str
        Path of directory to get file sizes.

    Returns
    -------
    git_files : dict
        Dictionary of ``{file : size}`` for each file tracked by git. 
    git_lfs_files : dict
        Dictionary of ``{file : size}`` for each file tracked by git lfs. 
    """

    try:
        repo = git.Repo(dir_path, search_parent_directories = True)   
        root = repo.working_tree_dir
    except:
        raise_from(CritError(messages.crit_error_no_repo), None)

    git_files = _get_file_sizes(dir_path, exclude = ['.git'])
    git_ignore_files = _get_git_ignore(repo)

    for ignore in git_ignore_files: 
        try:
            git_files.pop(ignore)
        except KeyError:
            pass
    
    lfs_list = _parse_git_attributes(os.path.join(root, '.gitattributes'))
    git_lfs_files = dict()
    
    for key in list(git_files.keys()):
        if _check_path_lfs(key, lfs_list):         
            git_lfs_files[key] = git_files.pop(key)
        
    return(git_files, git_lfs_files)


def _get_size_values(git_files, git_lfs_files):
    """.. Get file sizes for repository.

    Get file sizes for files in dictionary ``git_files`` and dictionary ``git_lfs_files``.

    Parameters
    ----------
    git_files : dict
        Dictionary of ``{file : size}`` for each file tracked by git. 
    git_lfs_files : dict
        Dictionary of ``{file : size}`` for each file tracked by git lfs. 

    Returns
    -------
    file_MB : float
        Size of largest file tracked by git in megabytes.
    total_MB : float
        Total size of files tracked by git in megabytes.
    file_MB : float
        Size of largest file tracked by git lfs in megabytes.
    total_MB : float
        Total size of files tracked by git lfs in megabytes.
    """

    file_MB = max(git_files.values() or [0])
    total_MB = sum(git_files.values() or [0]) 
    file_MB_lfs = max(git_lfs_files.values() or [0]) 
    total_MB_lfs = sum(git_lfs_files.values() or [0]) 

    size_list = [file_MB, total_MB, file_MB_lfs, total_MB_lfs]
    size_list = [size / (1024 ** 2) for size in size_list]

    return(size_list)


def check_module_size(paths):
    """.. Check file sizes for module.

    Checks file sizes for files to be committed in the current working directory. 
    Compares file sizes to size limits in file ``config`` and 
    produces warnings if any of the following limits are exceeded.

    - Individual size of a file tracked by git lfs (``file_MB_limit_lfs``)
    - Total size of all files tracked by git lfs (``total_MB_limit_lfs``)
    - Individual size of a file tracked by git (``file_MB_limit``)
    - Total size of all files tracked by git (``total_MB_limit``)
   
    Warning messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.

    Path Keys
    ---------
    config : str
        Path of project configuration file.   
    makelog : str
        Path of makelog.

    Returns
    -------
    None
    """
    
    try:
        git_files, git_lfs_files = _get_dir_sizes('.')
        file_MB, total_MB, file_MB_lfs, total_MB_lfs = _get_size_values(git_files, git_lfs_files)
    
        config = get_path(paths, 'config')
        config = open_yaml(config)
        max_file_sizes = config['max_file_sizes']
        
        print_message = ''
        if file_MB > max_file_sizes['file_MB_limit']:
            print_message = print_message + messages.warning_git_file_print % max_file_sizes['file_MB_limit']
        if total_MB > max_file_sizes['total_MB_limit']:
            print_message = print_message + messages.warning_git_repo % max_file_sizes['total_MB_limit']
        if file_MB_lfs > max_file_sizes['file_MB_limit_lfs']:
            print_message = print_message + messages.warning_git_lfs_file_print % max_file_sizes['file_MB_limit_lfs']
        if total_MB_lfs > max_file_sizes['total_MB_limit_lfs']:
            print_message = print_message + messages.warning_git_lfs_repo % max_file_sizes['total_MB_limit_lfs']
        print_message = print_message.strip()

        log_message = ''
        if file_MB > max_file_sizes['file_MB_limit']:
            log_message = log_message + messages.warning_git_file_log % max_file_sizes['file_MB_limit']
            exceed_files = [f for (f, s) in git_files.items() if s / (1024 ** 2) > max_file_sizes['file_MB_limit']]
            exceed_files = '\n'.join(exceed_files)
            log_message = log_message + '\n' + exceed_files
        if total_MB > max_file_sizes['total_MB_limit']:
            log_message = log_message + messages.warning_git_repo % max_file_sizes['total_MB_limit']
        if file_MB_lfs > max_file_sizes['file_MB_limit_lfs']:
            log_message = log_message + messages.warning_git_lfs_file_log % max_file_sizes['file_MB_limit_lfs']
            exceed_files = [f for (f, s) in git_lfs_files.items() if s / (1024 ** 2) > max_file_sizes['file_MB_limit_lfs']]
            exceed_files = '\n'.join(exceed_files)
            log_message = log_message + '\n' + exceed_files
        if total_MB_lfs > max_file_sizes['total_MB_limit_lfs']:
            log_message = log_message + messages.warning_git_lfs_repo % max_file_sizes['total_MB_limit_lfs']
        log_message = log_message.strip()

        if print_message:
            print(colored(print_message, metadata.color_failure))
        if log_message:
            write_to_makelog(paths, log_message)
    except:
        error_message = 'Error with `check_repo_size`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def _get_git_status(repo): 
    """.. Get git status.
    
    Get git status for repository ``repo``.

    Parameters
    ----------
    repo : :class:`git.Repo `
        Git repository to show working tree status.

    Returns
    -------
    file_list : list
        List of changed files in git repository according to git status.
    """
    
    root = repo.working_tree_dir

    file_list = repo.git.status(porcelain = True)
    file_list = file_list.split('\n')
    file_list = [f.lstrip().lstrip('MADRCU?!').lstrip() for f in file_list]
    file_list = [os.path.join(root, f) for f in file_list]
    file_list = [norm_path(f) for f in file_list]

    return(file_list)


def get_modified_sources(paths, 
                         source_map, 
                         depth = float('inf')):
    """.. Get source files considered changed by git.

    Checks the modification status for all sources contained in list 
    ``source_map`` (returned by :ref:`sourcing functions<sourcing functions>`). 
    Produces warning if sources have been modified according to git. 
    When walking through sources, float ``depth`` determines level of depth to walk. 
    Warning messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    source_map : list
        Mapping of sources (returned from :ref:`sourcing functions<sourcing functions>`).
    depth : float, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Returns
    -------
    overlap : list
        List of source files considered changed by git.

    Notes
    -----

    """
    
    try:
        source_list = [source for source, destination in source_map]
        source_list = [glob_recursive(source, depth) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)
   
        try:
            repo = git.Repo('.', search_parent_directories = True)    
        except:
            raise_from(CritError(messages.crit_error_no_repo), None)
        modified = _get_git_status(repo)

        overlap = [l for l in source_files if l in modified] 
            
        if overlap:
            if len(overlap) > 100:
                overlap = overlap[0:100]
                overlap = overlap + ["and more (file list truncated due to length)"]
            message = messages.warning_modified_files % '\n'.join(overlap)
            write_to_makelog(paths, message)
            print(colored(message, metadata.color_failure))
    except:
        error_message = 'Error with `get_modified_sources`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)

def check_conda_status(root):
    """.. Makes sure that the repository is being run with conda and is up to date.

    Checks that conda is activated. 
    Produces warning if it is not. 
    Produces warning if setup/conda_env.yaml has been altered more recently than the .

    Parameters
    ----------
    root : str 
        Directory of root.

    Returns
    -------
    None 

    Notes
    -----
    """

    check_conda = subprocess.Popen(['which', 'python'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)

    conda_out, conda_err = check_conda.communicate()

    # Check if currently in a conda env
    if 'conda' in str(conda_out):
        try:
            conda_info     = os.path.join(root, '.conda_info')
            conda_info_new = os.path.join(root, '.conda_info_new')

            if os.path.exists(conda_info):
                os.system('conda list --export > %s' % conda_info_new)
                if filecmp.cmp(conda_info, conda_info_new):
                    os.system('rm %s' % conda_info_new)
                else:
                    os.system('rm %s' % conda_info)
                    os.system('mv %s %s' % (conda_info_new, conda_info))

                info_time = os.path.getmtime(conda_info)
                info_time = datetime.fromtimestamp(info_time)

                conda_yaml = os.path.join(root, 'setup', 'conda_env.yaml')
                yaml_time = os.path.getmtime(conda_yaml)
                yaml_time = datetime.fromtimestamp(yaml_time)

                if yaml_time > info_time:
                    print(colored(messages.warning_old_conda, 'red'))
            else:
                os.system('conda list --export > %s' % conda_info)
        except:
            error_message = 'Error with `check_conda_status`. Traceback can be found below.' 
            error_message = format_message(error_message) 
            raise_from(ColoredError(error_message, traceback.format_exc()), None)
    else:
        print(colored(messages.warning_not_conda, 'red'))

__all__ = ['check_module_size', 'get_modified_sources', 'check_conda_status']
