#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import glob
from itertools import chain
import subprocess

from gslab_make.private.exceptionclasses import CritError
import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.utility import norm_path, file_to_array


class LinkDirective(object):
    """ 
    Directive for creating symlink(s).
    
    Notes
    -----
    Parse line of text containing linking instructions and represent as directive.
    Takes glob-style wildcards.
    
    Parameters
    ----------
    line : str
        Line of text containing linking instructions.
    link_dir : str
        Directory to write symlink(s).
    osname : str, optional
        Name of OS. Defaults to `os.name`.

    Attributes
    ----------
    target : list
        List of targets parsed from line.
    symlink : list
        List of symlinks parsed from line.
    link_list
        List of (target, symlink) mappings parsed from line.
    """
    
    def __init__(self, line, link_dir, osname = os.name):
        self.line      = line
        self.link_dir  = link_dir
        self.osname    = osname
        self.check_os()
        self.get_paths()
        self.check_paths()
        self.get_link_list()

    def check_os(self):
        """ Check OS is either POSIX or NT.  
                
        Returns
        -------
        None
        """      
        
        if self.osname not in {'posix', 'nt'}:
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):
        """ Parse targets and symlinks from line. 
                
        Returns
        -------
        None
        """
        
        try:
            line_parsed = self.line.strip().split('|')
            line_parsed = [l.strip() for l in line_parsed]
            line_parsed = [l.strip('"\'') for l in line_parsed]
            self.symlink, self.target = line_parsed
        except:
            raise CritError(messages.crit_error_bad_link % self.line)

        self.target = norm_path(self.target)
        self.symlink = norm_path(os.path.join(self.link_dir, self.symlink))

    def check_paths(self):
        """ Check targets and symlinks exist and have same number of wildcards. 
                
        Returns
        -------
        None
        """
    
        if re.findall('\*', self.target)!= re.findall('\*', self.symlink):
            raise SyntaxError(messages.syn_error_wildcard)
        
        if re.search('\*', self.target):
            if not glob.glob(self.target):
                raise CritError(messages.crit_error_no_path_wildcard % self.target)
        else:
            if not os.path.exists(self.target):
                raise CritError(messages.crit_error_no_path % self.target)   

    def get_link_list(self):
        """ Interpret wildcards to get list of paths that meet criteria. 
                
        Returns
        -------
        None
        """
    
        if re.match('\*', self.target):
            self.target_list  = glob.glob(self.target)
            self.symlink_list = [extract_wildcards(t) for t in self.target_list]
            self.symlink_list = [fill_in_wildcards(s) for s in self.symlink_list]
        else:
            self.target_list  = [self.target]
            self.symlink_list = [self.symlink]

        self.link_list = list(zip(self.target_list, self.symlink_list))

    def extract_wildcards(self, f):
        """ Extract wildcard characters from target path.
    
        Notes
        -----
        Suppose path `foo.py` and glob pattern `*.py`. 
        The wildcard characters would therefore be `foo`.
        
        Parameters
        ----------
        f : str
           Target path from which to extract wildcard characters.
           
        Returns
        -------
        wildcards : iter
           Iterator of extracted wildcard characters.
        """
        
        regex = self.target.split('*')
        regex = '(.*)'.join(regex) 

        wildcards = re.findall(regex, f)
        wildcards = [(w, ) if isinstance(w, str) else w for w in wildcards]
        wildcards = chain(*wildcards)

        return wildcards

    def fill_in_wildcards(self, wildcards):
        """ Fill in wildcards for symlink path.
        
        Notes
        -----
        Use extracted wildcard characters from a target path to create 
        corresponding symlink path.
    
        Parameters
        ----------
        wildcards: iterator
           Extracted wildcard characters (returned from `extract_wildcards`).
        
        Returns
        -------
        f : str
           Symlink path 
        """
        
        f = self.symlink
        for wild in wildcards:
            f = re.sub('\*', wild, f, 1)

        return f

    def create_symlinks(self):
        """ Create symlinks. 
                
        Returns
        -------
        None
        """
        
        if self.osname == 'posix':
            self.create_symlinks_posix()
        elif self.osname == 'nt':
            self.create_symlinks_nt()

        return(self.link_list)

    def create_symlinks_posix(self):   
        """ Create symlinks using POSIX shell command specified in metadata.  
        
        Returns
        -------
        None
        """
    
        for target, symlink in self.link_list:
            command = metadata.commands[self.osname]['makelink'] % (target, symlink)
            subprocess.Popen(command, shell = True)

    def create_symlinks_nt(self):   
        """ Create symlinks using NT shell command specified in metadata. 
                
        Returns
        -------
        None
        """
        for target, symlink in self.link_list:
            if os.path.isdir(target):
                directory = '/d'
            else:
                directory = ''

            command = metadata.commands[self.osname]['makelink'] % (directory, symlink, target)
            subprocess.Popen(command, shell = True)


class LinksList(object):
    """ 
    List of symlink directives.
    
    Notes
    -----
    Parse files containing linking instructions and represent as symlink directives.
    
    Parameters
    ----------
    file_list : list
        List of files from which to parse linking instructions.
    file_format : str
        Format of files from which to parse linking instructions.
    link_dir : str
        Directory to write symlink(s).
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.
        
    Attributes
    ----------
    link_directive_list : list
        List of symlink directives.   
    """
    
    def __init__(self, 
                 file_list, 
                 file_format,
                 link_dir, 
                 mapping_dict = {}):
        
        self.file_list = file_list
        self.file_format = file_format
        self.link_dir = link_dir
        self.mapping_dict = mapping_dict
        self.parse_file_list()
        self.get_paths()
        self.get_link_directive_list()

    def parse_file_list(self): 
        """ Parse wildcards in list of files. 
                
        Returns
        -------
        None
        """
        
        if type(self.file_list) is not list:
            raise TypeError(messages.type_error_file_list)

        file_list_parsed = [f for file in self.file_list for f in glob.glob(file)]   
        if file_list_parsed:
            self.file_list = file_list_parsed
        else:
            error_list = [str(f) for f in self.file_list]
            raise CritError(messages.crit_error_no_files % str(error_list))

    def get_paths(self):    
        """ Normalize paths. 
                
        Returns
        -------
        None
        """
        
        self.link_dir  = norm_path(self.link_dir)
        self.file_list = [norm_path(f) for f in self.file_list]

    def get_link_directive_list(self):
        """ Parse list of files to create symlink directives. 
                
        Returns
        -------
        None
        """
        
        lines = [line for file in self.file_list for line in file_to_array(file, self.file_format)]
        try:
            lines = [str(line).format(**self.mapping_dict) for line in lines]
        except KeyError as e:
            raise CritError(message.crit_error_path_mapping % str(e).strip("'"))

        self.link_directive_list = [LinkDirective(line, self.link_dir) for line in lines]

    def create_symlinks(self):       
        """ Create symlinks according to directives. 
        
        Returns
        -------
        link_map : list
            List of (target, symlink) for each symlink created.
        """
        
        link_map = []
        for link in self.link_directive_list:
            link_map.extend(link.create_symlinks())
            
        return link_map