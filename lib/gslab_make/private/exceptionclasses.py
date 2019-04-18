#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

from termcolor import colored

class CritError(Exception):
    pass

class ColoredError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return colored(self.value, color = 'green')