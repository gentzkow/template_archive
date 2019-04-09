#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import yaml
import git

import gslab_make.private.messages as messages

def convert_size_to_bytes(size_str):
    """ Convert human readable size to bytes. """
		
	multipliers = {
        ' B': 1024 ** 0,
        'KB': 1024 ** 1,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
    }

    for suffix in multipliers:
        if size_str.endswith(suffix):
            size = float(size_str[0:-len(suffix)]) * multipliers[suffix]
            return size
            
def parse_git_ls(text):
    """ Parse git ls-tree. """

    text = text.split()
    
    file = text[4]
    size = text[3]
    size = float(size)
    
    return (file, size)
    
def parse_lfs_ls(text):
    """ Parse git lfs ls-files. """

    text = text.split(' ', 2)[2].rsplit('(', 1)
    
    file = text[0].strip()
    size = text[-1].strip(')')
    size = convert_size_to_bytes(size)
    
    return (file, size)
   
def check_repository_size(paths):
    """ Check file sizes for repository.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'config' : str
                Path of config file.
        }

    Returns
    -------
    None
    """
    
    repo = git.Repo('.', search_parent_directories = True)    
    g = git.Git(repo)
            
    files = g.execute('git ls-tree -r -l HEAD', shell = True).split('\n')
    files = [parse_git_ls(f) for f in files]
    files = {file: size for (file, size) in files}
    
    lfs_files = g.execute('git lfs ls-files --size', shell = True).split('\n')
    lfs_files = [parse_lfs_ls(f) for f in lfs_files]
    lfs_files = {file: size for (file, size) in lfs_files}
    
    for key in lfs_files.keys():
        files.pop(key, None)
    
    file_MB_limit = max(files.values()) / (1024 ** 2)
    total_MB_limit = sum(files.values()) / (1024 ** 2)
    file_MB_limit_lfs = max(lfs_files.values()) / (1024 ** 2)
    total_MB_limit_lfs = sum(lfs_files.values()) / (1024 ** 2)
    
    config = yaml.load(open(paths['config'], 'rb'))
    max_file_sizes = config['max_file_sizes']
    
    if file_MB_limit      > max_file_sizes['file_MB_limit']:
        print(messages.warning_git_file % max_file_sizes['file_MB_limit']")
    if total_MB_limit     > max_file_sizes['total_MB_limit']:
        print(messages.warning_git_repo % max_file_sizes['total_MB_limit'])
    if file_MB_limit_lfs  > max_file_sizes['file_MB_limit_lfs']:
        print(messages.warning_git_file_lfs % max_file_sizes['file_MB_limit_lfs']")
    if total_MB_limit_lfs > max_file_sizes['total_MB_limit_lfs']:
        print(messages.warning_git_file_repo % max_file_sizes['total_MB_limit_lfs'])
                                