#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import yaml
import git
import traceback

from gslab_make.private.exceptionclasses import CritError
import gslab_make.private.messages as messages
from gslab_make.private.utility import norm_path, format_error, glob_recursive
from gslab_make.write_logs import write_to_makelog

def convert_size_to_bytes(size):
    """ Convert human readable size information to bytes. """
        
    multipliers = {
        ' B': 1024 ** 0,
        'KB': 1024 ** 1,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
    }

    for suffix in multipliers:
        if size.endswith(suffix):
            size = float(size[0:-len(suffix)]) * multipliers[suffix]
            return size
    

def parse_git_ls(text):
    """ Parse git ls-tree. """

    text = text.split()
    
    file = text[4]
    size = text[3]
    size = float(size)
    
    return (file, size)
    

def parse_git_lfs_ls(text):
    """ Parse git lfs ls-files. """

    text = text.split(' ', 2)[2].rsplit('(', 1)
    
    file = text[0].strip()
    size = text[-1].strip(')')
    size = convert_size_to_bytes(size)
    
    return (file, size)
   

def get_repo_size(repo):
    """ Get file sizes for repository.
    
    Parameters
    ----------
    repo : git.Repo 
        Git repository to get file sizes.

    Returns
    -------
    (git_files, git_lfs_files) : list
        git_files : dict
            Dictionary of {file : size} for each file tracked by git. 
        git_lfs_files : dict
            Dictionary of {file : size} for each file tracked by git lfs. 
    """

    g = git.Git(repo)
        
    git_files = g.execute('git ls-tree -r -l HEAD', shell = True).split('\n')
    git_files = [parse_git_ls(f) for f in git_files]
    git_files = {file: size for (file, size) in git_files}

    git_lfs_files = g.execute('git lfs ls-files --size', shell = True).split('\n')
    git_lfs_files = [parse_git_lfs_ls(f) for f in git_lfs_files]
    git_lfs_files = {file: size for (file, size) in git_lfs_files}

    for key in git_lfs_files.keys():
        git_files.pop(key, None)

    return (git_files, git_lfs_files)


def check_repo_size(paths):
    """ Check file sizes for repository.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'config' : str
                Path of config file.
            'makelog' : str
                Path of makelog.
        }

    Returns
    -------
    None
    """
    
    try:
        repo = git.Repo('.', search_parent_directories = True) 
        git_files, git_lfs_files = get_repo_size(repo)

        file_MB = max(git_files.values()) / (1024 ** 2)
        total_MB = sum(git_files.values()) / (1024 ** 2)
        file_MB_lfs = max(git_lfs_files.values()) / (1024 ** 2)
        total_MB_lfs = sum(git_lfs_files.values()) / (1024 ** 2)
    
        config = yaml.load(open(paths['config'], 'rb'))
        max_file_sizes = config['max_file_sizes']
        
        message = ''
        if file_MB > max_file_sizes['file_MB_limit']:
            message = message + '\n' + messages.warning_git_file % max_file_sizes['file_MB_limit']
        if total_MB > max_file_sizes['total_MB_limit']:
            message = message + '\n' + messages.warning_git_repo % max_file_sizes['total_MB_limit']
        if file_MB_lfs > max_file_sizes['file_MB_limit_lfs']:
            message = message + '\n' + messages.warning_git_lfs_file % max_file_sizes['file_MB_limit_lfs']
        if total_MB_lfs > max_file_sizes['total_MB_limit_lfs']:
            message = message + '\n' + messages.warning_git_lfs_repo % max_file_sizes['total_MB_limit_lfs']

        message = format_error(message)
        write_to_makelog(paths, message)
        print(message)
    except:
        error_message = 'Error with `check_repo_size`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise

def get_git_status(repo): 
    """ Get git status.
    
    Parameters
    ----------
    repo : git.Repo 
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
    file_list = [root + "/" + f for f in file_list]
    file_list = [norm_path(f) for f in file_list]

    return(file_list)


def get_modified_sources(paths, 
                         move_map, 
                         recursive = float('inf')):
    """ Get source files considered changed by git status.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    move_map : list 
        Mapping of symlinks/copies (destination) to sources (returned from `MoveList.create_symlinks` or `MoveList.create_copies`).
    recursive : int, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Returns
    -------
    overlap : list
        List of source files considered changed by git status.
    """
    
    try:
        source_list = [source for source, destination in move_map]
        source_list = [glob_recursive(source, recursive) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)
   
        try:
            repo = git.Repo('.', search_parent_directories = True)    
        except:
            raise CritError(messages.crit_error_no_repo)
        modified = get_git_status(repo)

        overlap = [l for l in source_files if l in modified] 
            
        if overlap:
            if len(overlap) > 100:
                overlap = overlap[0:100]
                overlap = overlap + ["and more (file list truncated due to length)"]
            message = format_error(messages.warning_modified_files % '\n'.join(overlap))
            write_to_makelog(paths, message)
            print(message)
    except:
        error_message = 'Error with `get_modified_sources`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise
                                