# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from, string_types
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import sys
import shutil
import traceback
import fileinput

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError, ProgramError
from gslab_make.private.programdirective import Directive, ProgramDirective, SASDirective, LyXDirective
from gslab_make.private.utility import get_path, format_message, norm_path
from gslab_make.write_logs import write_to_makelog


def run_jupyter(paths, program, timeout = None, kernel_name = ''):
    """.. Run Jupyter notebook using system command.

    Runs notebook ``program`` using Python API, with notebook specified 
    in the form of ``notebook.ipynb``. 
    Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    timeout : int, optional
        Time to wait (in seconds) to finish executing a cell before raising exception. 
        Defaults to no timeout.
    kernel_name : str, optional
        Name of kernel to use for execution 
        (e.g., ``python2`` for standard Python 2 kernel, ``python3`` for standard Python 3 kernel). 
        Defaults to ``''`` (i.e., kernel specified in notebook).

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_jupyter(paths, program = 'notebook.ipynb')
    """

    try:
        program = norm_path(program)

        with open(program) as f:
            message = 'Processing notebook: `%s`' % program
            write_to_makelog(paths, message)    
            print(colored(message, 'cyan'))
            
            if not kernel_name:
                kernel_name = 'python%s' % sys.version_info[0]
            ep = ExecutePreprocessor(timeout = timeout, kernel_name = kernel_name)
            nb = nbformat.read(f, as_version = 4)       
            ep.preprocess(nb, {'metadata': {'path': '.'}})
            
        with open(program, 'wt') as f:
            nbformat.write(nb, f)
    except:
        error_message = 'Error with `run_jupyter`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)



def run_lyx(paths, program, doctype = '', **kwargs): 
    """.. Run LyX script using system command.

    Compiles document ``program`` using system command, with document specified 
    in the form of ``script.lyx``. Status messages are appended to file ``makelog``. 
    PDF outputs are written in directory ``output_dir``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.
    doctype : str, optional
        Type of LyX document. Takes either ``'handout'`` and ``'comments'``. 
        All other strings will default to standard document type. 
        Defaults to ``''`` (i.e., standard document type).

    Path Keys
    ---------
    makelog : str
        Path of makelog.
    output_dir : str
        Directory to write PDFs.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_lyx(paths, program = 'script.lyx')
    """

    try:
        makelog = get_path(paths, 'makelog')
        output_dir = get_path(paths, 'output_dir')
        direct = LyXDirective(output_dir = output_dir, application = 'lyx', program = program, makelog = makelog, **kwargs)
            
        # Make handout/commented LyX file        
        if direct.doctype:
            temp_name = os.path.join(direct.program_name + '_' + direct.doctype)
            temp_program = os.path.join(direct.program_dir, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(direct.program, temp_program) 

            # ACTION ITEM: DEBUG ANDREFACTOR
            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True          
                if direct.doctype == 'handout' and beamer and (r'\options' in line):
                    line = line.rstrip('\n') + ', handout\n'
                elif direct.doctype == 'comments' and (r'\begin_inset Note Note' in line):
                    line = line.replace('Note Note', 'Note Greyedout')
        else:
            temp_name = direct.program_name
            temp_program = direct.program

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, temp_program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'LyX program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)

        # Move PDF output
        temp_pdf = os.path.join(direct.program_dir, temp_name + '.pdf')
        output_pdf = os.path.join(direct.output_dir, direct.program_name + '.pdf')

        if temp_pdf != output_pdf:
            shutil.copy2(temp_pdf, output_pdf)
            os.remove(temp_pdf)
            
        # Remove handout/commented LyX file
        if direct.doctype:
            os.remove(temp_program)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_lyx`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_mathematica(paths, program, **kwargs):
    """.. Run Mathematica script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.m``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_mathematica(paths, program = 'script.m')
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'math', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program, direct.option)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Mathematica program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_mathematica`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_matlab(paths, program, **kwargs):
    """.. Run Matlab script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.m``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_matlab(paths, program = 'script.m')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'matlab', program = program, makelog = makelog, **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.program_name + '.log')
        exit_code, stderr = direct.execute_command(command)   
        if exit_code != 0:
            error_message = 'Matlab program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        direct.move_program_output(program_log, direct.log)   
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_matlab`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_perl(paths, program, **kwargs):
    """.. Run Perl script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.pl``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_perl(paths, program = 'script.pl')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'perl', program = program, makelog = makelog, **kwargs)
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Perl program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_perl`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_python(paths, program, **kwargs):
    """.. Run Python script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.py``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_python(paths, program = 'script.py')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'python', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log() 
        if exit_code != 0:
            error_message = 'Python program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_python`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_r(paths, program, **kwargs):
    """.. Run R script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.R``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_r(paths, program = 'script.R')
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'r', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()      
        if exit_code != 0:
            error_message = 'R program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_r`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_sas(paths, program, lst = '', **kwargs):
    """.. Run SAS script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.sas``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.
    lst : str, optional
        Path of program lst. Program lst is only written if specified. 
        Defaults to ``''`` (i.e., not written).

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_sas(paths, program = 'script.sas')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = SASDirective(application = 'sas', program = program, makelog = makelog, **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), direct.program_name + '.lst')
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)       
        exit_code, stderr = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'SAS program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        direct.move_program_output(program_log)
        direct.move_program_output(program_lst)        
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_sas`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_stat_transfer(paths, program, **kwargs):
    """.. Run StatTransfer script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.stc`` or ``script.stcmd``. 
    Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_stat_transfer(paths, program = 'script.stc')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'st', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'StatTransfer program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stat_transfer`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_stata(paths, program, **kwargs):
    """.. Run Stata script using system command.

    Runs script ``program`` using system command, with script specified 
    in the form of ``script.do``. Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    program : str
        Path of script to run.

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Note
    ----
    When a do-file contains a space in its name, different version of Stata save the
    corresponding log file with different names. Some versions of Stata truncate the 
    name to everything before the first space of the do-file name.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of program log. Program log is only written if specified. 
        Defaults to ``''`` (i.e., not written). 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in :ref:`default settings<default settings>`.
    option : str, optional
        Options for system command. Defaults to options specified in :ref:`default settings<default settings>`.
    args : str, optional
        Not applicable.

    Returns
    -------
    None

    Example
    -------
    .. code-block:: python

        run_stata(paths, program = 'script.do')
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'stata', program = program, makelog = makelog, **kwargs)

        # Get program output (partial)
        program_name = direct.program.split(" ")[0]
        program_name = os.path.split(program_name)[-1]
        program_name = os.path.splitext(program_name)[0]
        program_log_partial = os.path.join(os.getcwd(), program_name + '.log')
        
        # Get program output (full)
        program_log_full = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Sanitize program 
        if direct.osname == "posix":
            direct.program = re.escape(direct.program)

        # Execute
        command = metadata.commands[direct.osname]['stata'] % (direct.executable, direct.option, direct.program)
        exit_code, stderr = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'Stata program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        try:
            output = direct.move_program_output(program_log_partial, direct.log)
        except:
            output = direct.move_program_output(program_log_full, direct.log)
        _check_stata_output(output)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stata`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
    
    
def _check_stata_output(output):
    """.. Check Stata output"""
    
    regex = "end of do-file[\s]*r\([0-9]*\);"
    if re.search(regex, output):
        error_message = 'Stata program executed with errors.'
        error_message = format_message(error_message)
        raise_from(ProgramError(error_message, 'See makelog for more detail.'), None)
        

def execute_command(paths, command, **kwargs):
    """.. Run system command.

    Runs system command `command` with shell execution boolean ``shell``. 
    Outputs are appended to file ``makelog`` and written to system command log file ``log``. 
    Status messages are appended to file ``makelog``.

    Parameters
    ----------
    paths : dict
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    command : str
        System command to run.
    shell : `bool`, optional
        See `here <https://docs.python.org/3/library/subprocess.html#frequently-used-arguments>`_. 
        Defaults to ``True``.
    log : str, optional
        Path of system command log. System command log is only written if specified. 
        Defaults to ``''`` (i.e., not written).

    Path Keys
    ---------
    makelog : str
        Path of makelog.

    Note
    ----
    We recommend leaving all other parameters to their defaults.

    Other Parameters
    ----------------
    osname : str, optional
        Name of OS. Used to check if OS is supported. Defaults to ``os.name``.


    Returns
    -------
    None

    Example
    -------
    The following code executes the ``ls`` command, 
    writes outputs to system command log file ``'file'``, 
    and appends outputs and/or status messages to ``paths['makelog']``.

    .. code-block:: python

        execute_command(paths, 'ls', log = 'file')
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = Directive(makelog = makelog, **kwargs)

        # Execute
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()   
        if exit_code != 0:
            error_message = 'Command executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `execute_command`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_module(root, module, build_script = 'make.py', osname = None):
    """.. Run module. 
    
    Runs script `build_script` in module directory `module` relative to root of repository `root`.

    Parameters
    ----------
    root : str 
        Directory of root.
    module: str
        Name of module.
    build_script : str
        Name of build script. Defaults to ``make.py``.
    osname : str, optional
        Name of OS. Used to determine syntax of system command. Defaults to ``os.name``.

    Returns
    -------
    None
    
    Example
    -------
    The following code runs the script ``root/module/make.py``.

    .. code-block:: python

        run_module(root = 'root', module = 'module')
    """

    osname = osname if osname else os.name # https://github.com/sphinx-doc/sphinx/issues/759

    try:
        module_dir = os.path.join(root, module)
        os.chdir(module_dir)

        build_script = norm_path(build_script)
        if not os.path.isfile(build_script):
            raise CritError(messages.crit_error_no_file % build_script)  

        message = 'Running module `%s`' % module
        message = format_message(message)
        message = colored(message, attrs = ['bold'])
        print('\n' + message)  

        status = os.system('%s %s' % (metadata.default_executables[osname]['python'], build_script))
        if status != 0:
            raise ProgramError()
    except ProgramError:
        sys.exit()
    except:
        error_message = 'Error with `run_module`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


__all__ = ['run_stata', 'run_matlab', 'run_perl', 'run_python', 
           'run_jupyter', 'run_mathematica', 'run_stat_transfer', 
           'run_lyx', 'run_r', 'run_sas', 'execute_command', 'run_module']