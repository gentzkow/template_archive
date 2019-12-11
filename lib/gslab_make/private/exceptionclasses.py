#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata

def string_encode(string, encoding = ''):
    if (sys.version_info < (3, 0)):
        string = string.encode('utf-8')  

    return(string)


class CritError(Exception):
    pass

class ColoredError(Exception):
    """ Colorized error messages. """
    
    def __init__(self, message = '', trace = ''):
        message = string_encode(message)
        message = '\n\n' + colored(message, color = metadata.color_failure)
        if trace:
            trace = string_encode(trace)
            trace = '\n\n' + colored(trace, color = metadata.color_failure)
            super(ColoredError, self).__init__(message + trace)
        else:
            super(ColoredError, self).__init__(message)
            
class ProgramError(ColoredError):
    """ Program execution exception. """
    pass