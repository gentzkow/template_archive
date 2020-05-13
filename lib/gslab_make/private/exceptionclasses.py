# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
import codecs

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata

"""
For some fixes Exception printing and I have no idea why...
"""

import subprocess
process = subprocess.Popen('', shell = True)
process.wait()

def decode(string):
    """Decode string."""

    if (sys.version_info < (3, 0)) and isinstance(string, string_types):
        string = codecs.decode(string, 'latin1')

    return(string)


def encode(string):
    """Clean string for encoding."""

    if (sys.version_info < (3, 0)) and isinstance(string, unicode):
        string = codecs.encode(string, 'utf-8') 

    return(string)


class CritError(Exception):
    pass

class ColoredError(Exception):
    """Colorized error messages."""
    
    def __init__(self, message = '', trace = ''):
        if message:
            message = decode(message)
            message = '\n\n' + colored(message, color = metadata.color_failure)  
        if trace:
            trace = decode(trace)
            message += '\n\n' + colored(trace, color = metadata.color_failure)
        
        super(ColoredError, self).__init__(encode(message))
            
class ProgramError(ColoredError):
    """Program execution exception."""
    
    pass