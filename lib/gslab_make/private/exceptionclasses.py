#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

from termcolor import colored

class CritError(Exception):
    pass

class ColoredError(Exception):
    def __init__(self, message, traceback):
        message = '\n\n' + colored(message, color = 'red')
        traceback = '\n\n' + colored(traceback, color = 'red')
        super(ColoredError, self).__init__(message + traceback)

class ProgramError(ColoredError):
    pass