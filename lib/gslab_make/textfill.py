#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import argparse
import types
import traceback
try:
	from html.parser import HTMLParser
except:
	from HTMLParser import HTMLParser
from gslab_make.private.exceptionclasses import CritError

import gslab_make.textfill_info as textfill_info

def textfill(**kwargs):
    try:
        args = parse_arguments(kwargs)
        text = parse_text(args)
        insert_text(args, text)
        exitmessage = args['template'] + ' filled successfully by textfill'
        print(exitmessage)
        return exitmessage	
        
    except:
        print('Error Found')
        exitmessage = traceback.format_exc()
        print(exitmessage)
        return exitmessage    

# Set textfill's docstring as the text in "textfill_info.py"
textfill.__doc__ = textfill_info.__doc__   
     

def parse_arguments(kwargs):
    args = dict()
    if 'input' in kwargs.keys():
        input_list = kwargs['input'].split()
        args['input'] = input_list
    if 'template' in kwargs.keys():
        args['template'] = kwargs['template']
    if 'output' in kwargs.keys():
        args['output'] = kwargs['output'] 
    if 'remove_echoes' in kwargs.keys():
        args['remove_echoes'] = kwargs['remove_echoes']
    else:
        args['remove_echoes'] = False
    if 'size' in kwargs.keys():
        args['size'] = kwargs['size']
    else:
        args['size'] = 'Default'
    if 'prefix' in kwargs.keys():
        args['prefix'] = kwargs['prefix'] + "_"
    else:
        args['prefix'] = 'textfill_'
    
    return args


def parse_text(args):
    text = read_text(args['input'], args['prefix'])
    text = clean_text(text, args['remove_echoes'])
    
    return text


def read_text(input, prefix):
    data = ''
    if isinstance(input, types.StringTypes):
        input = [input]
    for file in input:
        data += open(file, 'rU').read()
    text = text_parser(prefix)
    text.feed(data)
    text.close()
    
    return text


class text_parser(HTMLParser):
    def __init__(self, prefix):
        HTMLParser.__init__(self)
        self.recording = False
        self.results = {}
        self.open = []
        self.closed = []
        self.prefix = prefix
    
    def handle_starttag(self, tag, attrs):
        if tag.startswith(self.prefix):
            tag_name = tag.replace(self.prefix, '', 1)
            self.recording = True
            self.results[tag_name] = ''
            self.open.append(tag_name)
    
    def handle_data(self, data):
        if self.recording:
            self.results[self.open[-1]]+=data
    
    def handle_endtag(self, tag):
        if tag.startswith(self.prefix):
            tag_name = tag.replace(self.prefix, '', 1)
            self.open.remove(tag_name)
            self.closed.append(tag_name)
            if not self.open:
                self.recording = False
    
    def close(self):
        for tag in self.results.keys():
            if tag not in self.closed:
                raise CritError('Tag %s is not closed' % tag)


def clean_text(text, remove_echoes):
    for key in text.results:
        data = text.results[key].split('\n')
        if remove_echoes:
            data = filter(lambda x: not x.startswith('.'), data)
        else:
            data = filter(lambda x: not x.startswith('. insert_tag'), data)
        data = remove_trailing_leading_blanklines(data)
        text.results[key] = '\n'.join(data)
    
    return text


def remove_trailing_leading_blanklines(list):
    while list and not list[0]:
        del list[0]
    while list and not list[-1]:
        del list[-1]
    
    return list


def insert_text(args,text):
    lyx_text = open(args['template'], 'rU').readlines()
    # Loop over (expanding) raw LyX text
    n = 0
    loop = True
    while loop==True:
        n+=1 
        if n<len(lyx_text):
            if (lyx_text[n].startswith('name "text:')):
                tag = lyx_text[n].replace('name "text:','',1).rstrip('"\n').lower()
                if tag in text.results:
                    # Insert text after preceding layout is closed
                    insert_now = False
                    i = n
                    while insert_now is False:
                        i+=1
                        if lyx_text[i]=='\\end_layout\n':
                            insert_now = True
                    
                    # Insert text
                    for key in text.results:
                        if tag==key:
                            lyx_code = write_data_to_lyx(text.results[key], args['size'])
                    lyx_text.insert(i+1, lyx_code)
        else:
            loop = False
    
    outfile = open(args['output'], 'wb')
    outfile.write( ''.join(lyx_text) )
    outfile.close()
    
    return lyx_text


def write_data_to_lyx(data, size):
    data_list = data.split('\n')
    linewrap_beg = '\\begin_layout Plain Layout\n'
    linewrap_end = '\\end_layout\n'
    if size!='Default':
        size_line = '\\backslash\n' + size + '\n' + linewrap_end + linewrap_beg
    else:
        size_line = ''
    
    preamble = '\\begin_layout Plain Layout\n' \
               '\\begin_inset ERT status collapsed\n' \
               '\\begin_layout Plain Layout\n' + size_line + \
               '\\backslash\nbegin{verbatim}\n' \
               '\end_layout'
    postamble = '\\begin_layout Plain Layout\n' \
                '\\backslash\nend{verbatim}\n' \
                '\end_layout\n' \
                '\end_inset\n' \
                '\end_layout'
    
    lyx_code = preamble
    for line in data_list:
        lyx_code += linewrap_beg + line + linewrap_end
    lyx_code += postamble
    
    return lyx_code
