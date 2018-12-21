'''
#################################################################
#  textfill_readme.txt - Help/Documentation for textfill.py
#################################################################

Description:
textfill.py is a python module designed to copy sections of log files produced 
by Stata to LyX files.

Usage:
Textfill takes as input log files produced by Stata (the input files) and a LyX 
file with labels indicating where logs should be inserted (the template file), 
and produces a LyX file (the output file) which includes sections of the input 
files (as indicated by tags inside the input files) in the locations indicated 
by the labels in the template file.

Textfill must first be imported to make.py.  This is typically achieved by 
including the following lines:

```
from gslab_fill.textfill import textfill
```

Once the module has been imported, the syntax used to call textfill is as follows:

```
textfill( input = 'input_file(s)', template = 'template_file', output = 'output_file', 
          [size = 'size'], [remove_echoes = 'True/False'] )
```

The argument 'input' is a list of the text files containing the stata logs to be 
copied to the LyX tables. If there are multiple input text files, they are listed as: 
input = 'input_file_1 input_file_2'. The argument 'template' is the user written LyX 
file which contains the labels which will be replaced with sections of the log files. 
The argument 'output' is the name of the filled LyX file to be produced. Note that this 
file is created by textfill.py, and should not be edited manually by the user.

There are two optional arguments: 'size' and 'remove_echoes'. The argument 'size' 
determines the size of inserted text relative to body text in the output file. 
It accepts LaTeX font size arguments, and defaults to same size as body. The argument 
'remove_echoes' determines whether or not Stata command echoes are removed from the 
copied log.  It defaults to false.


###########################
Input File Format:
###########################

Input files for textfill.py are log files produced by Stata. Sections of input files 
to be inserted by textfill are indicated by tags printed by the stata command 
'insert_tags', which is defined by a gslab ado file in gslab-econ/gslab_stata/gslab_misc/.

In the stata do file which produces the input logs, the user begins a tagged section 
with the command: 
insert_tag tag_name, open

This will insert the following line, which indicates the beginning of a tagged section 
of the log, into the log file:
`<textfill_tag_name>`

The user should now add lines to the do file which print the output they want to add to 
the tagged section, followed by the line:
insert_tag tag_name, close

This inserts the following line to the log file, indicating the end of the tagged section:
`</textfill_tag_name>`


###########################
Template LyX Format:
###########################

The LyX template file contains labels which determine where the tagged sections of the 
input files are inserted. To insert a log section tagged as 'tag_name', in a particular 
place in the LyX file, the user inserts a label object with the value 'text:tag_name' 
inside a 'Text' custom inset.  The 'text:' part of the label is mandatory. When textfill 
is run, the tagged section of the input files will be inserted as text input at the 
location of corresponding label in the LyX file.

Note that the 'Text' custom inset object is available from 'Insert > Custom Insets' when 
Lyx had been reconfigured with the custom module text.module. This module is available on 
the repo at /admin/Computer Build Sheet/, and can be installed according to the instructions
in /admin/Computer Build Sheet/standard_build.pdf.

Note that label/tag names cannot be duplicated.  For a single template file, each block of 
text to be inserted must have a unique label, and there must be one, and only one, section 
of the input files tagged with that same label. Having multiple sections of the input files 
or multiple labels in the template file with the same name will cause errors.  

Note also that when a LyX file with a 'text:' label is opened in LyX, or when textfill.py is 
run on it, LyX may issue a warning: 
"The module text has been requested by this document but has not been found..."

This warning means that the custom module text.module has not been installed - see above.


#####################
# Example
#####################

The following is an example of code, which could appear in a Stata do file, used to produce 
input for textfill.
```
insert_tag example_log, open
display "test"
insert_tag example_log, close
```

Suppose output from Stata is being logged in stata.log.  This code adds the following lines 
to stata.log:

```
. insert_tag example_log, open
<example_log>

. display "test"
test

. insert_tag example_log, close
</example_log>
```

Suppose we have a LyX file, template.lyx, which contains a label with the value 
"text:example_log"  (without the ""). The following textfill command,
`textfill( input = 'stata.log', template = 'template.lyx', output = 'output.lyx' )`

would produce a file, output.lyx, identical to template.lyx, but with the label 
"text:example.log" replaced with the verbatim input:

```
. display "test"
test
```

The following command,
`textfill( input = 'stata.log', template = 'template.lyx', 
           output = 'output.lyx', remove_echoes = True )`

would produce output.lyx replacing the label with the verbatim input (removing Stata command echoes):


`test`


######################
# Error Logging
######################

If an error occurs during the call to text, it will be displayed in the command window.  
When make.py finishes, the user will be able to scroll up through the output and examine 
any error messages.  Error messages, which include a description of the error type
and a traceback to the line of code where the error occurred, can also be returned as a 
string object using the following syntax:

```
exitmessage = textfill( input = 'input_file(s)', template = 'template_file', output = 'output_file', 
                        [size = 'size'], [remove_echoes = 'True/False'] )
```

Lines can then be added to make.py to output this string to a log file using standard 
Python and built in gslab_make commands.
'''
