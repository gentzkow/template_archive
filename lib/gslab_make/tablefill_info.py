'''
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
'''
