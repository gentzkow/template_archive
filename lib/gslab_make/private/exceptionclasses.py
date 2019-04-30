#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

from termcolor import colored
import colorama
colorama.init()

class CritError(Exception):
    pass

class ColoredError(Exception):
    def __init__(self, message, trace):
        message = '\n\n' + colored(message, color = 'red')
        trace = '\n\n' + colored(trace, color = 'red')
        super(ColoredError, self).__init__(message + trace)

class ProgramError(ColoredError):
    pass