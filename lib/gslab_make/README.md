# Paths

<b>
The majority of the functions in </b><code>gslab_make</code><b> contain a </b><code>paths</code><b> argument that requires passing in a dictionary specifying default paths used for writing and logging purposes. The dictionary <i>must</i> contain values for the following keys (i.e., default paths):
</b>

> * `config`
>
>     * Default path for config file. 
>
> * `config_user`
>
>     * Default path for config user file. 
> 
> * `input_dir` 
> 
>     * Default path for writing symbolic links/copies to sources internal to the repository. 
>
> * `external_dir` 
> 
>     * Default path for writing symbolic links/copies to sources external to the repository. 
>    
> * `output_dir` 
> 
>     * Default path for finding outputs for logging.
>
> * `pdf_dir` 
> 
>     * Default path for writing LyX documents. 
>
> * `makelog`
> 
>     * Default path for writing make log.
>
> * `output_statslog`
> 
>     * Default path for writing log containing output statistics.
>
> * `output_headslog`
> 
>     * Default path for writing log containing output headers.
>
> * `source_maplog`
> 
>     * Default path for writing log containing source mappings.
>
> * `source_statslog` 
> 
>     * Default path for writing log containing source statistics.
>
> * `source_headslog`
> 
>     * Default path for writing log containing source headers.   

<ul>
<b>Note:</b>
<br> 
To suppress writing any specific log (<code>makelog</code>, <code>output_statslog</code>, <code>output_headslog</code>, <code>source_maplog</code>, <code>source_statslog</code>, <code>source_headslog</code>), set the key for that log to <code>''</code>.

<br>
<br>
<b>Example:</b>
<br>
The following default paths are recommended:
<pre>
    paths = {
        'config'          : '../config.yaml',      # Adjust relative path accordingly
        'config_user'     : '../config_user.yaml', # Adjust relative path accordingly
        'input_dir'       : 'input/',
        'external_dir'    : 'external/',
        'output_dir'      : 'output/',
        'pdf_dir'         : 'output/',
        'makelog'         : 'log/make.log',
        'output_statslog' : 'log/output_stats.log',
        'output_headslog' : 'log/output_heads.log', 
        'source_maplog'   : 'log/source_map.log',
        'source_statslog' : 'log/source_stats.log',
        'source_headslog' : 'log/source_heads.log'
    }
</pre>
</ul>

<br> 

<b>
The following functions will specify which default paths in </b><code>paths</code><b> are required in their documentation. For example, </b><code>function(paths = {pdf_dir, makelog})</code><b> uses the default paths corresponding to </b><code>paths['pdf_dir']</code><b> and </b><code>paths['makelog']</code><b>.
</b>

<br> 

# Repository checking functions

<b>The following functions are used to check file size and modification status of files tracked by git. The logs are intended to facilitate proper committing activity.</b>

<br>

<pre>
check_repo.<b>check_module_size(</b><i> 
    paths = {
        config, 
        makelog
    },</i><b>
)</b>
</pre>
> Compares sizes for files in the current directory `.`. Produces warning if any of the following size statistics are larger than limits set in config file `config`:
>
> * Individual size of a file tracked by git lfs (`file_MB_limit_lfs`)
>
> * Total size of all files tracked by git lfs (`total_MB_limit_lfs`)
>
> * Individual size of a file tracked by git (`file_MB_limit`)
>
> * Total size of all files tracked by git (`total_MB_limit`)
>
> Warning messages are appended to make log `makelog`.

<br>

<pre>
check_repo.<b>get_modified_sources(</b><i> 
    paths = {
        makelog
    },
    move_map, 
    depth = float('inf'),</i><b>
)</b>
</pre>
> Checks the modification status for sources contained in all mappings of list `move_map` (returned by `move_sources.link_inputs`, `move_sources.copy_inputs`, `move_sources.link_externals`). Produces warning if sources have been modified according to git. When walking through sources, float `depth` determines level of depth to walk. Warnings are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>get_modified_sources(paths, move_map, depth = 1)</code> will check modification status for all source files listed in <code>move_map</code>.
<br>
<br>
<code>get_modified_sources(paths, move_map, depth = 2)</code> will check modification status for all source files listed in <code>move_map</code>, and all files contained in any source directories listed in <code>move_map</code>.
<br>
<br>
<code>get_modified_sources(paths, move_map, depth = float('inf'))</code> will check modification status for all source files listed in <code>move_map</code>, and all files contained in any level of source directories listed in <code>move_map</code>.
</ul>

<br> 

# Logging functions

<b>The following functions are used to create a master log of activity (i.e., a <i>make log</i>) and to log information about output files. The logs are intended to facilitate the reproducibility of research.</b>

<br>

<pre>
write_logs.<b>start_makelog(</b><i>paths = {makelog}</i><b>)</b>
</pre>
> Starts new make log at file `makelog`, recording start time. Sets start condition for make log to boolean `True`, which is needed by other functions to confirm make log exists.

<br>

<pre>
write_logs.<b>end_makelog(</b><i>paths = {makelog}</i><b>)</b>
</pre>
> Ends make log at file `makelog`, recording end time. 

<br>

<pre>
write_logs.<b>log_files_in_output(</b><i> 
    paths = {
        output_dir, 
        output_statslog,
        output_headslog, 
        makelog
    }, 
    depth = float('inf'),</i><b>
)</b>
</pre>
> Logs the following information for all files contained in directory `output_dir`:
>
> * File name (in file `output_statslog`)
>
> * Last modified (in file `output_statslog`)
>
> * File size (in file `output_statslog`)
>
> * File head (in file `output_headslog`)
>
> When walking through directory `output_dir`, float `depth` determines level of depth to walk. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>write_output_logs(paths, depth = 1)</code> will log information for all files contained in <code>paths['output_dir']</code>.
<br>
<br>
<code>write_output_logs(paths, depth = 2)</code> will log information for all files contained in <code>paths['output_dir']</code>, and all files contained in any directories in <code>paths['output_dir']</code>.
<br>
<br>
<code>write_output_logs(paths, depth = float('inf'))</code> will log information for all files contained in any level of <code>paths['output_dir']</code>.
</ul>

<br>

# Linking functions

<b>The following functions are used to create symbolic links to source files. Doing so avoids potential duplication of source files and any associated confusion. In the case of modules dedicated to LyX documents, there is a optional function to copy source files instead of creating symbolic links so that users without </b><code>gslab_make</code><b> can still manually compile.</b>

<br>

<pre>
move_sources.<b>link_inputs(</b><i>
    paths = {
        input_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Symbolic links are written in directory `input_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>link_inputs(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create symbolic links.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Symbolic links <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['input_dir']</code>. Their targets would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following symbolic links in <code>paths['input_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>link_externals(</b><i>
    paths = {
        external_dir,
        makelog,
    }, 
    file_list, 
    path_mappings</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Symbolic links are written in directory `external_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>link_externals(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create symbolic links.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Symbolic links <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['external_dir']</code>. Their targets would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following symbolic links in <code>paths['external_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>copy_inputs(</b><i>
    paths = {
        input_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create copies using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Copies are written in directory `input_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create copies (destinations) from orginals (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>copy_inputs(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create copies.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Copies <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['input_dir']</code>. Their originals would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following copies in <code>paths['input_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>copy_externals(</b><i>
    paths = {
        external_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create copies using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Copies are written in directory `external_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create copies (destinations) from orginals (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>copy_externals(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create copies.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Copies <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['external_dir']</code>. Their originals would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following copies in <code>paths['external_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

# Source logging functions

<b>The following function is used to log linking/copying activity and information about source files. The logs are intended to facilitate the reproducibility of research.</b>

<br>

<pre>
write_source_logs.<b>write_source_logs(</b><i>
    paths = {
        source_statslog,
        source_headslog, 
        source_maplog,
        makelog,
    }, 
    move_map, 
    depth = float('inf')</i><b>
)</b>
</pre>

> Logs the following information for files contained in all mappings of list `move_map` (returned by `move_sources.link_inputs`, `move_sources.copy_inputs`, `move_sources.link_externals`):
> 
> * Mapping of symbolic links/copies to sources (in file `source_maplog`)
>
> * Details on files contained in sources:          
>
>     * File name (in file `source_statslog`)
>
>     * Last modified (in file `source_statslog`)
>
>     * File size (in file `source_statslog`)
>
>     * File head (in file `source_headslog`)
>
> When walking through sources, float `depth` determines level of depth to walk. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>write_source_logs(paths, move_map, depth = 1)</code> will log information for all source files listed in <code>move_map</code>.
<br>
<br>
<code>write_source_logs(paths, move_map, depth = 2)</code> will log information for all source files listed in <code>move_map</code>, and all files contained in any source directories listed in <code>move_map</code>.
<br>
<br>
<code>write_source_logs(paths, move_map, depth = float('inf'))</code> will log information for all source files listed in <code>move_map</code>, and all files contained in any level of source directories listed in <code>move_map</code>.
</ul>

<br> 

# Program functions

<b>The following functions are used to run programs for certain applications. Unless specified otherwise, the program functions will use default settings to run your program. See the setting section below for more information.</b>

<br>

<pre>
run_program.<b>run_jupyter(</b><i>
    paths = {makelog}, 
    program, 
    timeout = None, 
    kernel_name = ''</i><b>
)</b>
</pre>
> Runs notebook `program` using Python API, with notebook specified in the form of `'notebook.ipynb'`. Status messages are appended to make log `makelog`.
>
> Jupyter-specific settings:
>
> * `timeout` : int
>
>     * Maximum time in seconds to execute a cell before throwing exception. Defaults to no timeout.
>
> * `kernel_name` : str
>
>     * Name of kernel to use for execution (e.g., `'python2'` for standard Python 2 kernel, `'python3'` for standard Python 3 kernel). Defaults to kernel specified in notebook.

<ul>
<b>Example:</b>
<br>
<code>run_jupyter(paths, program = 'notebook.ipynb')</code>
</ul>

<br>

<pre>
run_program.<b>run_lyx(</b><i>
    paths = {makelog, pdf_dir}, 
    program, 
    doctype = ''
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.lyx'`. Status messages are appended to make log `makelog`. PDF outputs are written in directory `pdf_dir`.
>
> LyX-specific settings:
>
> * `doctype` : str
>
>     * Type of LyX document. Takes either `handout` and `comments`. Defaults to no special document type.

<ul>
<b>Example:</b>
<br>
<code>run_lyx(paths, program = 'script.lyx')</code>
</ul>

<br>

<pre>
run_program.<b>run_mathematica(</b><i>
    paths = {makelog}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_mathematica(paths, program = 'script.m')</code>
</ul>

<br>

<pre>
run_program.<b>run_matlab(</b><i>
     paths = {makelog}, 
     program, 
     *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_matlab(paths, program = 'script.m')</code>
</ul>

<br>

<pre>
run_program.<b>run_perl(</b><i>
    paths = {makelog}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.pl'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_perl(paths, program = 'script.pl')</code>
</ul>

<br>

<pre>
run_program.<b>run_python(</b><i>
    paths = {makelog}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.py'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_python(paths, program = 'script.py')</code>
</ul>

<br>

<pre>
run_program.<b>run_r(</b><i>
    paths = {makelog}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.R'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_r(paths, program = 'script.R')</code>
</ul>

<br>

<pre>
run_program.<b>run_sas(</b><i>
    paths = {makelog}, 
    program, 
    lst = '', 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.sas'`. Status messages are appended to make log `makelog`.
>
> SAS-specific settings:
>
> * `lst` : str
>
>     * Path of program lst to write outputs. Defaults to <code>''</code> (i.e., not written).
>

<ul>
<b>Example:</b>
<br>
<code>run_sas(paths, program = 'script.sas')</code>
</ul>

<br>

<pre>
run_program.<b>run_stat_transfer(</b><i>
    paths = {makelog}, 
    program,
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.stc'` or `'script.stcmd'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_stat_transfer(paths, program = 'script.stc')</code>
</ul>

<br>

<pre>
run_program.<b>run_stata(</b><i>
    paths = {makelog}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.do'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_stata(paths, program = 'script.do')</code>
</ul>

<br>

<b>The following function is used to run system commands.</b>

<br>

<pre>
run_program.<b>execute_command(</b><i>
    paths = {makelog}, 
    command, 
    osname = os.name, 
    shell = False, 
    log = ''</i><b>
)</b>
</pre>
> Runs system command `command`, assuming operating system `osname` and shell execution boolean `shell`. Outputs are appended to make log file `makelog` and written to program log file `log`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b> 
<br>
For more information on shell execution, see <a href = 'https://docs.python.org/2/library/subprocess.html#frequently-used-arguments'>here</a>.
<br>
<br>
By default, program log is not written as <code>log = ''</code>.
<br>
<br>
<b>Example:</b> 
<br>
<code>execute_command(paths, 'ls', log = 'file')</code> executes the <code>'ls'</code> command, writes outputs to program log <code>'file'</code>, and appends outputs and/or status messages to <code>path['makelog']</code>.
</ul>

<br>

<b>The following function is used to run a module.</b>

<br>

<pre>
run_program<b>.run_module(</b><i>root, module, build_script = 'make.py'</i><b>)</b> 
</pre>
> Runs script `build_script` in module `module` relative to root of repository `root`. `build_script` defaults to `make.py`.

<br>

#### Settings

* `osname` : str
    * Name of OS. Defaults to `os.name`.

* `shell` : bool
    * For more information on shell execution, see <a href = 'https://docs.python.org/2/library/subprocess.html#frequently-used-arguments'>here</a>.

* `log` : str
    * Path of program log to write outputs. Defaults to `''` (i.e., not written).

* `executable` : str
    * Executable to use for system command. Default executable depends on application.

    <pre>
    default_executables = {
        'posix': 
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'math'      : 'math',
             'matlab'    : 'matlab',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : 'stata-mp'},
        'nt': 
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'matlab'    : 'matlab',
             'math'      : 'math',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : '%STATAEXE%'}
    }
    </pre>

* `option` : str
    * Options for system command. Default option depends on application.

    <pre>
    default_options = {
        'posix': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'math'      : '-noprompt',
             'matlab'    : '-nosplash -nodesktop',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '', 
             'stata'     : '-e'},
        'nt': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'matlab'    : '-nosplash -minimize -wait',
             'math'      : '-noprompt',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '-nosplash', 
             'stata'     : '/e'}
    }
    </pre>

* `args`
    * Arguments for system command. Defaults to no arguments.

<br> 

# Utility functions

<b>The following functions are general utility functions for build scripts. Functions to update executable names/path_mappings and copy outputs are included.</b>

<br>

<pre>
make_utility.<b>update_executables(</b><i>paths = {config_user}</i>)</b> 
</pre>
> Updates executable names with executables listed in config user `config_user`
> 
<ul>
<b>Note:</b> 
<br>
Executable names are used by program functions.
</ul>

<br>

<pre>
make_utility.<b>update_mappings(</b><i>
    paths = {
        config_user
    }, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Updates dictionary `path_mappings` with externals listed in config user file `config_user`.
> 
<ul>
<b>Note:</b> 
<br>
Path mappings are used by linking functions.
</ul>

<br>

<pre>
make_utility.<b>copy_output(</b><i>file, copy_dir</i><b>)</b> 
</pre>
> Copies output `file` to directory `copy_dir` with user prompt to confirm copy.

<br>

# Directory functions

<b>The following functions are used to make modifications to a directory. Functions to check operating system, clear directories, and zip/unzip files are included.</b>

<br>

<pre>
modify_dir.<b>remove_dir(</b><i>dir_list</i><b>)</b>
</pre>
> Removes all directories in list <code>dir_list</code> using system command. Safely removes symbolic links.

<ul>
<b>Example:</b>
<br>
<code>remove_dir(['dir1', 'dir2'])</code> removes directories <code>'dir1'</code> and <code>'dir2'</code>. 
<br>
<br>
<b>Notes:</b>
<br>
Directories can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
</ul>

<br>

<pre>
modify_dir.<b>clear_dir(</b><i>dir_list</i><b>)</b>
</pre>
> Clears all directories in list <code>dir_list</code> using system command. Safely clears symbolic links.

<ul>
<b>Example:</b>
<br>
<code>clear_dir(['dir1', 'dir2'])</code> clears directories <code>'dir1'</code> and <code>'dir2'</code>. 
<br>
<br>
<b>Notes:</b>
<br>
To clear a directory means to remove all contents of a directory. If the directory is nonexistent, the directory is created.
<br>
<br>
Directories can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
</ul>

<br>

<pre>
modify_dir.<b>unzip(</b><i>zip_path, output_dir</i><b>)</b>
</pre>
> Unzips file `zip_path` into directory `output_dir`.

<br>

<pre>
modify_dir.<b>zip_dir(</b><i>source_dir, zip_dest</i><b>)</b>
</pre>
> Zips directory `source_dir` into file `zip_dest`. 

<br>