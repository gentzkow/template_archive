#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import ColoredError
from gslab_make.private.movedirective import MoveList
from gslab_make.private.utility import get_path, format_message
from gslab_make.write_logs import write_to_makelog


def _create_links(paths,
                  file_list):
    """.. Create symlinks from list of files containing linking instructions.

    Create symbolic links using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Symbolic links are written in directory ``move_dir``. Status messages are appended to file ``make log``.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format linking instructions.
    file_list : str, list
        File or list of files containing linking instructions.

    Path Keys
    ---------
    move_dir : str
        Directory to write links.
    makelog : str
        Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each symlink created.
    """
             
    move_dir = get_path(paths, 'move_dir')

    move_list = MoveList(file_list, move_dir, paths)
    if move_list.move_directive_list:
        os.makedirs(move_dir)
        source_map = move_list.create_symlinks()       
    else:
        source_map = []

    return(source_map)
        

def _create_copies(paths,
                   file_list):
    """.. Create copies from list of files containing copying instructions.

    Create copies using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Copies are written in directory ``move_dir``. Status messages are appended to file ``make log``.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format copying instructions.
    file_list : str, list
        File or list of files containing copying instructions.

    Path Keys
    ---------
    move_dir : str
        Directory to write copies.
    makelog : str
        Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each copy created.
    """
             
    move_dir = get_path(paths, 'move_dir')

    move_list = MoveList(file_list, move_dir, paths)
    if move_list.move_directive_list:
        os.makedirs(move_dir)
        source_map = move_list._create_copies()       
    else:
        source_map = []

    return(source_map)


def link_inputs(paths,
                file_list):
    """.. Create symlinks to inputs from list of files containing linking instructions. 

    Create symbolic links using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Symbolic links are written in directory ``input_dir``. Status messages are appended to file ``make log``.

    Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way.

    .. code-block:: md

        # Each line of instruction should contain a destination and source delimited by a `|`
        # Lines beginning with # are ignored
        destination | source

    .. Note::
        Symbolic links can be created to both files and directories.

    .. Note::
        Instruction files can be specified with the * shell pattern (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__). Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format linking instructions.
    file_list : str, list
        File or list of files containing linking instructions.

    Path Keys
    ---------
    input_dir : str
       Directory to write symlinks.
    makelog : str
       Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each symlink created.

    Example
    -------
    Suppose you call the following function. 

    .. code-block:: python

        link_inputs(paths, ['file1'], formatting_dict)

    Suppose ``paths`` contained the following values.

    .. code-block:: md

        paths = {'root': '/User/root/',
                 'makelog': 'make.log',
                 'input_dir': 'input'}

    Now suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | {root}/source1

    The ``{root}`` in the instruction file would be string formatted using ``paths``. Therefore, the function would parse the instruction as:

    .. code-block:: md

        destination1 | /User/root/source1

    Example
    -------
    The following code would use instruction files ``file1`` and ``file2`` to create symbolic links. 

    .. code-block:: python

        link_inputs(paths, ['file1', 'file2'])

    Suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | source1
        destination2 | source2

    Symbolic links ``destination1`` and ``destination1`` would be created in directory ``paths['input_dir']``. Their targets would be ``source1`` and ``source2``, respectively. 

    Example
    -------
    Suppose you have the following targets. 

    .. code-block:: md

        source1
        source2
        source3

    Specifying ``destination* | source*`` in one of your instruction files would create the following symbolic links in ``paths['input_dir']``.

    .. code-block:: md

        destination1
        destination2
        destination3
    """

    try:
        paths['move_dir'] = get_path(paths, 'input_dir')
        source_map = _create_links(paths, file_list)

        message = 'Input links successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))

        return(source_map)
    except:
        error_message = 'An error was encountered with `link_inputs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def link_externals(paths,
                   file_list):
    """.. Create symlinks to externals from list of files containing linking instructions. 

    Create symbolic links using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Symbolic links are written in directory ``external_dir``. Status messages are appended to file ``make log``.

    Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way.

    .. code-block:: md

        # Each line of instruction should contain a destination and source delimited by a `|`
        # Lines beginning with # are ignored
        destination | source

    .. Note::
        Symbolic links can be created to both files and directories.

    .. Note::
        Instruction files can be specified with the * shell pattern (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__). Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format linking instructions.
    file_list : str, list
        File or list of files containing linking instructions.

    Path Keys
    ---------
    external_dir : str
       Directory to write symlinks.
    makelog : str
       Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each symlink created.

    Example
    -------
    Suppose you call the following function. 

    .. code-block:: python

        link_externals(paths, ['file1'], formatting_dict)

    Suppose ``paths`` contained the following values.

    .. code-block:: md

        paths = {'root': '/User/root/',
                 'makelog': 'make.log',
                 'input_dir': 'input'}

    Now suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | {root}/source1

    The ``{root}`` in the instruction file would be string formatted using ``paths``. Therefore, the function would parse the instruction as:

    .. code-block:: md

        destination1 | /User/root/source1

    Example
    -------
    The following code would use instruction files ``file1`` and ``file2`` to create symbolic links. 

    .. code-block:: python

        link_externals(paths, ['file1', 'file2'])

    Suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | source1
        destination2 | source2

    Symbolic links ``destination1`` and ``destination1`` would be created in directory ``paths['external_dir']``. Their targets would be ``source1`` and ``source2``, respectively. 

    Example
    -------
    Suppose you have the following targets. 

    .. code-block:: md

        source1
        source2
        source3

    Specifying ``destination* | source*`` in one of your instruction files would create the following symbolic links in ``paths['external_dir']``.

    .. code-block:: md

        destination1
        destination2
        destination3
    """
    
    try:
        paths['move_dir'] = get_path(paths, 'external_dir')
        source_map = _create_links(paths, file_list)

        message = 'External links successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))

        return(source_map)
    except:
        error_message = 'An error was encountered with `link_externals`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_inputs(paths,
                file_list):
    """.. Create copies to inputs from list of files containing copying instructions. 

    Create copies using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Copies are written in directory ``input_dir``. Status messages are appended to file ``make log``.

    Instruction files on how to create copies (destinations) from targets (sources) should be formatted in the following way.

    .. code-block:: md

        # Each line of instruction should contain a destination and source delimited by a `|`
        # Lines beginning with # are ignored
        destination | source

    .. Note::
        Instruction files can be specified with the * shell pattern (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__). Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format copying instructions.
    file_list : str, list
        File or list of files containing copying instructions.

    Path Keys
    ---------
    input_dir : str
       Directory to write copies.
    makelog : str
       Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each copy created.

    Example
    -------
    Suppose you call the following function. 

    .. code-block:: python

        copy_inputs(paths, ['file1'], formatting_dict)

    Suppose ``paths`` contained the following values.

    .. code-block:: md

        paths = {'root': '/User/root/',
                 'makelog': 'make.log',
                 'input_dir': 'input'}

    Now suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | {root}/source1

    The ``{root}`` in the instruction file would be string formatted using ``paths``. Therefore, the function would parse the instruction as:

    .. code-block:: md

        destination1 | /User/root/source1

    Example
    -------
    The following code would use instruction files ``file1`` and ``file2`` to create copies. 

    .. code-block:: python

        copy_inputs(paths, ['file1', 'file2'])

    Suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | source1
        destination2 | source2

    Copies ``destination1`` and ``destination1`` would be created in directory ``paths['input_dir']``. Their targets would be ``source1`` and ``source2``, respectively. 

    Example
    -------
    Suppose you have the following targets. 

    .. code-block:: md

        source1
        source2
        source3

    Specifying ``destination* | source*`` in one of your instruction files would create the following copies in ``paths['input_dir']``.

    .. code-block:: md

        destination1
        destination2
        destination3
    """
    
    try:
        paths['move_dir'] = get_path(paths, 'input_dir')
        source_map = _create_copies(paths, file_list)

        message = 'Input copies successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))

        return(source_map)
    except:
        error_message = 'An error was encountered with `copy_inputs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_externals(paths,
                   file_list):
    """.. Create copies to externals from list of files containing copying instructions. 

    Create copies using instructions contained in files of list ``file_list``. Instructions are `string formatted <https://docs.python.org/3.4/library/string.html#format-string-syntax>`__ using paths dictionary ``paths``. Copies are written in directory ``external_dir``. Status messages are appended to file ``make log``.

    Instruction files on how to create copies (destinations) from targets (sources) should be formatted in the following way.

    .. code-block:: md

        # Each line of instruction should contain a destination and source delimited by a `|`
        # Lines beginning with # are ignored
        destination | source

    .. Note::
        Instruction files can be specified with the * shell pattern (see `here <https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html>`__). Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below. Dictionary additionally used to string format copying instructions.
    file_list : str, list
        File or list of files containing copying instructions.

    Path Keys
    ---------
    external_dir : str
       Directory to write copies.
    makelog : str
       Path of makelog.

    Returns
    -------
    source_map : list
        List of (source, destination) for each copy created.

    Example
    -------
    Suppose you call the following function. 

    .. code-block:: python

        copy_externals(paths, ['file1'], formatting_dict)

    Suppose ``paths`` contained the following values.

    .. code-block:: md

        paths = {'root': '/User/root/',
                 'makelog': 'make.log',
                 'input_dir': 'input'}

    Now suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | {root}/source1

    The ``{root}`` in the instruction file would be string formatted using ``paths``. Therefore, the function would parse the instruction as:

    .. code-block:: md

        destination1 | /User/root/source1

    Example
    -------
    The following code would use instruction files ``file1`` and ``file2`` to create copies. 

    .. code-block:: python

        copy_externals(paths, ['file1', 'file2'])

    Suppose instruction file ``file1`` contained the following text.

    .. code-block:: md

        destination1 | source1
        destination2 | source2

    Copies ``destination1`` and ``destination1`` would be created in directory ``paths['external_dir']``. Their targets would be ``source1`` and ``source2``, respectively. 

    Example
    -------
    Suppose you have the following targets. 

    .. code-block:: md

        source1
        source2
        source3

    Specifying ``destination* | source*`` in one of your instruction files would create the following copies in ``paths['external_dir']``.

    .. code-block:: md

        destination1
        destination2
        destination3
    """

    try:
        paths['move_dir'] = get_path(paths, 'external_dir')
        source_map = _create_copies(paths, file_list)

        message = 'External copies successfully created!'
        write_to_makelog(paths, message)    
        print(colored(message, metadata.color_success))
        
        return(source_map)
    except:
        error_message = 'An error was encountered with `copy_externals`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)