#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import shutil
import fileinput
import traceback
import re

import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ProgramError, ColoredError
from gslab_make.private.programdirective import Directive, ProgramDirective, SASDirective, LyXDirective
from gslab_make.private.utility import format_error, format_traceback
from gslab_make.write_logs import write_to_makelog


def run_stata(paths, program, **kwargs):
    """ Run Stata script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'stata', program = program, makelog = makelog, **kwargs)

        # Get program output
        program_name = direct.program.split(" ")[0]
        program_name = os.path.split(program_name)[-1]
        program_name = os.path.splitext(program_name)[0]
        program_log = os.path.join(os.getcwd(), program_name + '.log')
        
        # Sanitize program 
        if direct.osname == "posix":
            direct.program = re.escape(direct.program)

        # Execute
        command = metadata.commands[direct.osname]['stata'] % (direct.executable, direct.option, direct.program)
        exit_code, traceback = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'Stata program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
        output = direct.move_program_output(program_log, direct.log)
        check_stata_output(output)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stata`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
    
    
def check_stata_output(output):
    regex = "end of do-file[\s]*r\([0-9]*\);"
    if re.search(regex, output):
        raise ProgramError('Stata program executed with errors.', 'Check logs for more detail.')


def run_matlab(paths, program, **kwargs):
    """ Run Matlab script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
  
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'matlab', program = program, makelog = makelog, **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.program_name + '.log')
        exit_code, traceback = direct.execute_command(command)   
        if exit_code != 0:
            error_message = 'Matlab program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
        direct.move_program_output(program_log, direct.log)   
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_matlab`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_perl(paths, program, **kwargs):
    """ Run Perl script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'perl', program = program, makelog = makelog, **kwargs)
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Perl program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_perl`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())


def run_python(paths, program, **kwargs):
    """ Run Python script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'python', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, traceback = direct.execute_command(command)
        direct.write_log() 
        if exit_code != 0:
            error_message = 'Python program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_python`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_mathematica(paths, program, **kwargs):
    """ Run Mathematica script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
        
    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'math', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program, direct.option)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Mathematica program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_mathematica`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_stat_transfer(paths, program, **kwargs):
    """ Run StatTransfer script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'st', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'StatTransfer program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stat_transfer`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_lyx(paths, program, **kwargs): 
    """ Run LyX script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
            'pdf_dir' : str
                Directory to write PDFs.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    doctype : str, optional
       Type of Lyx document. Takes either `handout` and `comments`. 
       Defaults to no special document type.
        
    Returns
    -------
    None
    """
    
    makelog = paths['makelog']
    pdf_dir = paths['pdf_dir']

    try:
        direct = LyXDirective(pdf_dir = pdf_dir, application = 'lyx', program = program, makelog = makelog, **kwargs)
            
        # Make handout/commented LyX file        
        if direct.doctype:
            temp_name = os.path.join(direct.program_name + '_' + direct.doctype)
            temp_program = os.path.join(direct.program_dir, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(direct.program, temp_program) 

            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True          
                if direct.doctype == 'handout' and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif direct.doctype == 'comments' and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
                print(line)
        else:
            temp_name = direct.program_name
            temp_program = direct.program

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, temp_program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'LyX program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)

        # Move PDF output
        temp_pdf = os.path.join(direct.program_dir, temp_name + '.pdf')
        output_pdf = os.path.join(direct.pdf_dir, direct.program_name + '.pdf')

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
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_r(paths, program, **kwargs):
    """ Run R script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = ProgramDirective(application = 'r', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()      
        if exit_code != 0:
            error_message = 'R program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_r`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def run_sas(paths, program, **kwargs):
    """ Run SAS script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    lst : str, optional
        Path of program lst. Program lst is only written if specified. 
        
    Returns
    -------
    None
    """

    makelog = paths['makelog']

    try:
        direct = SASDirective(application = 'sas', program = program, makelog = makelog, **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), direct.program_name + '.lst')
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)       
        exit_code, error_message = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'SAS program executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
        direct.move_program_output(program_log)
        direct.move_program_output(program_lst)        
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_sas`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())
        

def execute_command(paths, command, **kwargs):
    """ Run system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    command : str
        system command to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of system command log. system command log is only written if specified. 
        
    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

    try:
        direct = Directive(makelog = makelog, **kwargs)

        # Execute
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()   
        if exit_code != 0:
            error_message = 'Command executed with errors. Traceback can be found below.'
            error_message = format_error(error_message)
            raise ProgramError(error_message, traceback)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `execute_command`. Traceback can be found below.' 
        error_message = format_error(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())