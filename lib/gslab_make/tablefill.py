#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import re
import traceback
from itertools import chain

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import convert_to_list, norm_path, format_message

def _parse_tag(tag):
    """.. Parse tag from input."""
    
    if not re.match('<Tab:(.*)>\n', tag, flags = re.IGNORECASE):
        raise Exception
    else:
        tag = re.sub('<Tab:(.*?)>\n', r'\g<1>', tag, flags = re.IGNORECASE)
        tag = tag.lower()
        
    return(tag)
    
    
def _parse_data(data, null):
    """.. Parse data from input.
    
    Parameters
    ----------
    data : list
        Input data to parse.
    null : str
        String to replace null characters.

    Returns
    -------
    data : list
        List of data values from input.
    """
    null_strings = ['', '.', 'NA']
     
    data = [row.rstrip('\r\n') for row in data]
    data = [row for row in data if row]
    data = [row.split('\t') for row in data]
    data = chain(*data)
    data = list(data)
    if (null != None):
        data = [null if value in null_strings else value for value in data]
    
    return(data)
        
    
def _parse_content(file, null):
    """.. Parse content from input."""
        
    with open(file, 'r') as f:
        content = f.readlines()
    try:
        tag = _parse_tag(content[0])
    except:
        raise_from(CritError(messages.crit_error_no_tag % file), None)   
    data = _parse_data(content[1:], null)
    
    return(tag, data)
    
    
def _insert_value(line, value, type):
    """.. Insert value into line.
    
    Parameters
    ----------
    line : str
        Line of document to insert value.
    value : str
        Value to insert.
    type : str
        Formatting for value.

    Returns
    -------
    line : str
        Line of document with inserted value.
    """
    
    if (type == 'no change'):
        line = re.replace('\\\\?#\\\\?#\\\\?#', value, line)
                          
    elif (type == 'round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)
        digits = re.findall('\\\\?#([0-9]+)\\\\?#', line)[0]
        rounded_value = format(value, '.%sf' % digits)
        line = re.sub('(.*?)\\\\?#[0-9]+\\\\?#', r'\g<1>' + rounded_value, line)
                      
    elif (type == 'comma + round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)
        digits = re.findall('\\\\?#([0-9]+),\\\\?#', line)[0]
        rounded_value = format(value, ',.%sf' % digits)
        line = re.sub('(.*?)\\\\?#[0-9]+,\\\\?#', r'\g<1>' + rounded_value, line)

    return(line)


def _insert_tables_lyx(template, tables):
    """.. Fill tables for LyX template.
    
    Parameters
    ----------
    template : str
        Path of LyX template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled LyX template.
    """

    with open(template, 'r') as f:
        doc = f.readlines()
      
    is_table = False

    for i in range(len(doc)):
        # Check if table
        if not is_table and re.match('name "tab:', doc[i]):
            tag = doc[i].replace('name "tab:','').rstrip('"\n').lower()      
            try:
                values = tables[tag]
                entry_count = 0
                is_table = True
            except KeyError:
                pass

        # Fill in values if table
        if is_table:
            try:
                if re.match('.*###', doc[i]):
                    doc[i] = _insert_value(doc[i], values[entry_count], 'no change')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+#', doc[i]):
                    doc[i] = _insert_value(doc[i], values[entry_count], 'round')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+,#', doc[i]):
                    doc[i] = _insert_value(doc[i], values[entry_count], 'comma + round')
                    entry_count += 1
                    break
                elif re.match('</lyxtabular>', doc[i]):
                    is_table = False
                    if entry_count != len(values):
                        raise_from(CritError(messages.crit_error_too_many_values % tag), None)
            except IndexError:
                raise_from(CritError(messages.crit_error_not_enough_values % tag), None)
                
    doc = '\n'.join(doc)
    
    return(doc)


def _insert_tables_latex(template, tables):
    """.. Fill tables for LaTeX template.
    
    Parameters
    ----------
    template : str
        Path of LaTeX template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled LaTeX template.
    """

    with open(template, 'r') as f:
        doc = f.readlines()

    is_table = False

    for i in range(len(doc)):
        # Check if table
        if not is_table and re.search('label\{tab:', doc[i]):
            tag = doc[i].split(':')[1].rstrip('}\n').strip('"').lower()
            try:
                values = tables[tag]
                entry_count = 0
                is_table = True
            except KeyError:
                pass

        # Fill in values if table
        if is_table:
            try:
                line = doc[i].split("&")
    
                for j in range(len(line)):
                    if re.search('.*\\\\#\\\\#\\\\#', line[j]):
                        line[j] = _insert_value(line[j], values[entry_count], 'no change')
                        entry_count += 1
                    elif re.search('.*\\\\#[0-9]+\\\\#', line[j]):
                        line[j] = _insert_value(line[j], values[entry_count], 'round')                   
                        entry_count += 1
                    elif re.search('.*\\\\#[0-9]+,\\\\#', line[j]):
                        line[j] = _insert_value(line[j], values[entry_count], 'comma + round')
                        entry_count += 1
                   
                doc[i] = "&".join(line)
    
                if re.search('end\{tabular\}', doc[i], flags = re.IGNORECASE):
                    is_table = False
                    if entry_count != len(values):
                        raise_from(CritError(messages.crit_error_too_many_values % tag), None)
            except IndexError:
                raise_from(CritError(messages.crit_error_not_enough_values % tag), None)

    doc = '\n'.join(doc)

    return(doc)


def _insert_tables(template, tables):
    """.. Fill tables for template.
    
    Parameters
    ----------
    template : str
        Path of template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled template.
    """
    
    if re.search('\.lyx', template):
        doc = _insert_tables_lyx(template, tables)
    elif re.search('\.tex', template):
        doc = _insert_tables_latex(template, tables)

    return(doc)


def tablefill(inputs, template, output, null = None):
    """.. Fill tables for template using inputs.
    
    Fills tables in document ``template`` using files in list ``inputs``. 
    Writes filled document to file ``output``. 
    Null characters in ``inputs`` are replaced with value ``null``.

    Parameters
    ----------
    inputs : list
        Input or list of inputs to fill into template.
    template : str
        Path of template to fill.
    output : str
        Path of output.
    null : str
        Value to replace null characters (i.e., ``''``, ``'.'``, ``'NA'``). Defaults to no replacement.

    Returns
    -------
    None
    
    Example
    -------

    .. code-block::

        #################################################################
        #  tablefill_readme.txt - Help/Documentation for tablefill.py
        #################################################################

        Description:
        tablefill.py is a Python module designed to fill LyX/Tex tables with output 
        from text files (usually output from Stata or Matlab).

        Usage:
        Tablefill takes as input a LyX (or Tex) file containing empty tables (the template 
        file) and text files containing data to be copied to  these tables (the 
        input  files), and produces a LyX (or Tex) file with filled tables (the output file). 
        For brevity, LyX will be used to denote LyX or Tex files throughout.

        Tablefill must first be imported to make.py.  This is typically achieved 
        by including the following lines:

        ```
        from gslab_fill.tablefill import tablefill
        ```

        Once the module has been imported, the syntax used to call tablefill is 
        as follows:

        ```
        tablefill(input = 'input_file(s)', template = 'template_file', 
                  output = 'output_file')
        ```

        The argument 'template' is the user written LyX file which contains the 
        tables to be filled in. The argument 'input' is a list of the text files 
        containing the output to be copied to the LyX tables. If there are multiple 
        input text files, they are listed as: input = 'input_file_1 input_file_2'. 
        The argument 'output' is the name of the filled LyX file to be produced.  
        Note that this file is created by tablefill.py and should not be edited 
        manually by the user.

        ###########################
        Input File Format:
        ###########################

        The data needs to be tab-delimited rows of numbers (or characters), 
        preceeded by  `<label>`.  The < and > are mandatory. The numbers can be 
        arbitrarily long, can be negative, and can also be in scientific notation.

        Examples:
        ----------

        ```
        <tab:Test>
        1   2   3
        2   3   1
        3   1   2
        ```

        ```
        <tab:FunnyMat>
        1   2   3   23  2
        2   3
        3   1   2   2
        1
        ```
        (The rows do not need to be of equal length.)

        Completely blank (no tab) lines are ignored.
        If a "cell" is merely "." or "[space]", then it is treated as completely 
        missing. That is, in the program:

        ```
        <tab:Test>
        1   2   3
        2   .   1   3
        3       1   2
        ```

        is equivalent to:
        ```
        <tab:Test>
        1   2   3
        2   1   3
        3   1   2
        ```

        This feature is useful as Stata outputs missing values in numerical 
        variables as ".", and missing values in string variables as "[space]".

        ................................
         Scientific Notation Notes:
        ................................
        The scientific notation ihas to be of the form:
        [numbers].[numbers]e(+/-)[numbers]

        Examples:
        ```
        23.2389e+23
        -2.23e-2
        -0.922e+3
        ```

        ###########################
        Template LyX Format:
        ###########################

        The LyX template file determines where the numbers from the input files are placed.

        Every table in the template file (if it is to be filled) must appear within a float. 
        There must  be one, and only one, table object inside the float, and the table name 
        must include a label  object that corresponds to the label of the required table in 
        the input file.

        Note that table names cannot be duplicated.  For a single template file, each table 
        to be filled must have a unique label, and there must be one, and only one, table with 
        that same label in the text files used as input. Having multiple tables with the
        same name in the input files or in the template file will cause errors.  

        Note also that labels are NOT case-sensitive. That is, <TAB:Table1> is considered
         the same as `<tab:table1>`.

        In the LyX tables, "cells" to be filled with entries from the input text files are 
        indicated by the following tags: 

        `"###"  (no quotes)`
        or 
        `"#[number][,]#"  (no quotes)`

        The first case will result in a literal substitution.  I.e. whatever is in the text 
        tables for that  cell will be copied over. The second case will convert the data 
        table's number (if in scientific notation) and will truncate this converted number 
        to [number] decimal places.  It will automatically round while doing so.

        If a comma appears after the number (within #[number]#), then it will add commas 
        to the digits to the left of the decimal place.

        Examples:
        ---------
        ```
        2309.2093 + ### = 2309.2093
        2309.2093 + #4# = 2309.2093
        2309.2093 + #5# = 2309.20930
        2309.2093 + #20# = 2309.20930000000000000000
        2309.2093 + #3# = 2309.209
        2309.2093 + #2# = 2309.21
        2309.2093 + #0# = 2309
        2309.2093 + #0,# = 2,309
        ```

        ```
        -2.23e-2  + #2# = -0.0223 + #2# = -0.02
        -2.23e-2  + #7# = -0.0223 + #7# = -0.0223000
        -2.23e+10  + #7,# = -22300000000 + #7,# = -22,300,000,000.000000
        ```

        Furthermore, only ###/#num# will be replaced, allowing you to put things around 
        ###/#num# to alter the final output:

        Examples:
        --------

        ```
        2309.2093 + (#2#) = (2309.21)
        2309.2093 + #2#** = 2309.21**
        2309.2093 + ab#2#cd = ab2309.21cd
        ```

        If you are doing exact substitution, then you can use characters:

        Examples:
        ---------
        `abc + ### = abc`

        ................................
         Intentionally blank cells:
        ................................

        If you would like to display a blank cell, you can use "---":

        Examples:
        ---------
        ```
        --- + ### = ---
        --- + #3# = ---
        ```

        ######################
        # Example Combinations 
        #   Of input + template
        ######################


        Example 1 (Simple)
        ----------
        ```
        Input: <tab:Test>
        1   2   3
        2   1   3
        3   1   2

        Template: `<tab:Test> ` (pretend this is what you see in LyX)

        ### ### ###
        ### ### ###
        ### ### ###

        Result:<tab:Test>
        1   2   3
        2   1   3
        3   1   2
        ```

        Example 2 (More Complicated)
        ----------
        ```
        Input: <tab:Test>
        1   .   3
        2e-5    1   3.023
        .   -1  2   3

        Template: <tab:Test>  (pretend this is what you see in LyX)
        (###)   2   ###
        #3# ### #1#
        NA  ### ### ###

        Result:<tab:Test>
        (1) 2   3
        0.000   1   3.0
        NA  -1  2   3
        ```

        ===================
        ====Important======
        ===================
        By design, missings in input table and "missings" in template do not have to 
        line up.

        Example 3 (LyX)
        ----------
        ```
        Input: <tab:Test>
        1   .   3
        2e-5    .   3.023
        .   -1  2

        Template: <tab:Test> 
        ### ### abc
        abc #2# #3#
        NA  ### ###

        Result:<tab:Test>
        1   3   abc
        abc 0.00    3.023
        NA  -1  2

        Recall that to the program, the above input table is no different from:
        1   3
        2e-5    3.023
        -1  2
        ```

        It doesn't "know" where the numbers should be placed within a row, only what 
        the next number to place should be.

        Similarly:

        Example 4 (LyX)
        ----------
        ```
        Input: <tab:Test>
        1   1   2
        1   1   3
        2   -1  2

        Template: <tab:Test>  
        ### ### ###
        abc abc abc
        ### #2# #3#
        ### ### ###

        Result:<tab:Test>
        1   1   2
        abc abc abc
        1   1.00    3.000
        2   -1  2
        ```

        If a row in the template has no substitutions, then it's not really a row from 
        the program's point of view.


        ######################
        # Error Logging
        ######################

        If an error occurs during the call to tablefill, it will be displayed in the 
        command window.  When make.py finishes, the user will be able to scroll up 
        through the output and examine any  error messages.  Error messages, which 
        include a description of the error type and a traceback to the line of code 
        where the error occured, can also be retuned as a string object using the 
        following syntax:

        exitmessage = tablefill( input = 'input_file(s)', template = 'template_file', 
                                 output = 'output_file' )

        Lines can then be added to make.py to output this string to a log file using 
        standard Python and built in gslab_make commands.


        ######################
        # Common Errors
        ######################

        Common mistakes which can lead to errors include:

        - Mismatch between the length of the LyX table and the corresponding text table.  
        If the LyX table has more entries to be filled than the text table has entries to
        fill from, this will cause an error and the table will not be filled.

        - Use of numerical tags (e.g. #1#) to fill non-numerical data.  This will cause 
        an error. Non-numerical data can only be filled using "###", as it does not make 
        sense to round or truncate this data.

        - Multiple table objects in the same float.  Each table float in the template LyX 
        file can only contain one table object.  If a float contains a second table object, 
        this table will not be filled.


        ######################
        # Boldfacing entries
        ######################

        It is straightforward to develop functions that conditionally write entries of 
        tables in boldface; functions may do so by inserting '\series bold' in the lines
        of the filled LyX file immeadiately before phrases that the user wishes to make bold.
    """

    try:
        inputs = convert_to_list(inputs, 'file')
        inputs = [norm_path(file) for file in inputs]
        content = [_parse_content(file, null) for file in inputs]
        tables = {tag:data for (tag, data) in content}
        if (len(content) != len(tables)):
            raise_from(CritError(messages.crit_error_duplicate_tables), None)

        doc = _insert_tables(template, tables)  
        
        with open(output, 'w') as f:
            f.write(doc)
    except:
        error_message = 'Error with `tablefill`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


__all__ = ['tablefill']