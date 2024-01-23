
<p style="font-family:courier;font-weight:900;font-size:30px">
    GentzkowLabTemplate
</p>

  1. [Overview](#overview)
  2. [Requirements](#requirements)
  3. [Setup](#setup)
  4. [Repository organization](#repository-organization)
  5. [Recommended practices](#recommended-practices)
  6. [FAQ](#faq)

</br>
</br>


# Overview

This repository template is designed to provide a simple, extendable, and
reproducible framework that allows teams of researchers to to collaborate
using multiple software tools (e.g., Python, R, Stata, Latex) across multiple 
platforms (Linux/MacOS, Windows).

To learn more about the principles behind the template, see [Code and Data for
the Social Sciences: A Practitioner's Guide](http://web.stanford.edu/~gentzkow/research/CodeAndData.pdf),
by Matthew Gentzkow and Jesse Shapiro.

The template is distributed under the [MIT license](https://github.com/gentzkow/GentzkowLabTemplate/blob/main/LICENSE.txt). 


# Requirements

To run out of the box, the template requires:
* Python 3.x
* LaTex

The template assumes that your Python executable is `python3`. If not, the 
setup script will produce an error and prompt you to update `local_env.sh` 
with the correct name of your Python executable. The example scripts assume that
you have `pandas`, `numpy`, `statsmodels`, and `matplotlib` installed.

The [Setup](#setup) section below describes how to use the template 
with other tools, including R and Stata, as well as
how to use the template without Python and/or Latex installed. 


# Setup

Here are the basic steps to set up and run the template on Linux/MacOS.

```sh
# Clone the repo, cd into it
git clone https://github.com/gentzkow/GentzkowLabTemplate
cd GentzkowLabTemplate

# Run setup script to create local settings file local_env.sh,
# and check that local executables are correctly installed.
bash setup.sh

# Run the `make.sh` script at the root of the repository to 
# check that the template runs without error
bash make.sh
```

On **Windows**, the steps are the same, but you will need to use a Bash emulator
such as [Git Bash](https://gitforwindows.org/) to execute the shell scripts. 

To create your own repository from the template, navigate to the template's
[GitHub page](https://github.com/gentzkow/GentzkowLabTemplate) and click `Use this template`.
See the [GitHub documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
for more details.

For illustration purposes, the template includes sample data building and
analysis scripts in Python, R, and Stata, and sample files to create slides
and paper drafts in Latex. The R and Stata scripts are commented out by default,
so that the template will run out of the box with only Python and Latex installed.

To use the template with **R**, uncomment the lines beginning `run_R` in
`1_data/source/make.sh` and `2_analysis/source/make.sh`. The R Studio executable 
must be callable from the command line. The template assumes
that the executable is `rstudio`. If your executable has a different name,
you will need to update it in the `local_env.sh` file created by `setup.sh`. The
example scripts assume that you have `tidyverse`, `stargazer`, and `ggplot2` installed. 

To use the template with **Stata**, uncomment the lines beginning `run_stata` in
`1_data/source/make.sh` and `2_analysis/source/make.sh`. The Stata executable 
must be callable from the command line. The template assumes
that the executable is `StataMP`. If your executable has a different name,
you will need to update it in the `local_env.sh` file created by `setup.sh`.

To use the template with **other tools, such as Julia, Matlab, or Lyx**, you will
need to add lines to the `make.sh` files to run the relevant scripts, following the same
format as the `run_python`, `run_R`, and `run_stata` commands in the deafult `make.sh`
files.

To use the template **without Python**, comment out the lines beginning `run_python` in
`1_data/source/make.sh` and `2_analysis/source/make.sh`. 

To use the template **without Latex**, comment out the lines beginning `run_latex` in
`3_slides/source/make.sh` and `4_paper/source/make.sh`.


# Repository organization

## Overview

* `README.txt`: This readme file.
* `LICENSE.txt`: The template's MIT License.
* `setup.sh`: Creates `local_env.sh` at the root of the repository and checks that repository requirements are met.
* `run_all.sh`: Runs the repository from beginning to end
* `local_env.sh`: Stores settings and paths specific to a user's local environment. This file is not committed to Git.
* `/lib/`: Contains code libraries/packages that are used across multiple parts of the repository.
* `/0_raw/`: Contains raw data, images, etc. that are inputs to the code downstream and are committed to the repository.
* `/1_data/`: Wrangles the data
* `/2_analysis/`: Runs the analysis.
* `/3_slides/`: Makes the slides.
* `/4_paper/`: Makes the paper.

## Modules

The template is organized into *modules*. A module is a subdirectory with a `make.sh` script at its root, a `/source/` subdirectory,
and an `/output/` subdirectory. Each module is a self-contained unit that runs code in `/source/` to produce output in
`/output/`. If a module uses inputs beyond the code itself (e.g., data stored elsewhere in the repository and/or externally), these
are controlled by the script `get_inputs.sh`, which creates an `/input/` subdirectory with symlinks and/or copies of the relevant inputs.

Out of the box, the template contains 4 modules, `1_data`, `2_analysis`, `3_slides`, and `4_paper`. The subdirectory `0_raw` is not a module
because it does not contain code.

## Make.sh scripts

The script `make.sh` runs a given module from beginning to end. More specifically, it:

* Loads local settings and paths from `local_env.sh`
* Loads shell commands from `/lib/shell/`
* Clears the `/output/` directory
* Runs `get_inputs.sh` to populate the `/input/` directory
* Runs the scripts in `/source/` with a sequence of command-line calls 
* Logs everything in `/output/make.log`

The calls to the individual scripts are governed by a set of shell commands named `run_python`, 
`run_R`, etc. that are defined in `lib/shell/`. These are very simple wrappers that
issue the appropriate command line calls to run a given script. You could replace these 
with direct command-line calls -- for example, you could replace the line

```
run_python wrangle_data.py ../$LOGFILE
```

in `1_data/make.sh` with

```
python3 wrangle_data.py >> ../$LOGFILE
```

The advantages of using the wrapper commands include:

* They use executable names defined by `local_env.sh`, so that the code can work across machines with different local configurations
* They clean up LaTex auxiliary files
* They copy Latex output files to the `output` directory, whereas `pdflatex` places output in the same directory as the code by default
* They copy default Stata logs into `/output/make.log`
* They handle differences in Stata command line syntax across operating systems
* They handle cases where scripts terminate with errors in a friendly way


# Recommended practices

## Managing software dependencies

TBD

## Keeping inputs and outputs clear

Code in a module's `/source/` directory should only call inputs from the module's `/input/` directory, or, in the case ofinputs that are produced within the module itself, from `/output/` or `temp` (see [here](#working-with-temporary-or-intermediate-files) for more detail on `/temp/` directories. **Code should never reference files elsewhere in the repository, or files external to the repository, directly**.

The module's `input` directory should be populated by the module's `get_inputs.sh` script. It should never be modified directly by the user.

All output should be placed the module's `/output/` directory.

Benefits of following these rules include:
* The input-output structure of each module is transparent to the user
* Modules are self-contained and the code is agnostic about the location of files in the local directory structure
* `make.sh` can log the state of the inputs at the time when the module was run
* `make.sh` can guarantee that all contents of `/output/` were produced by a single run of the code
* If the location of an input file changes, this can be updated once in `get_inputs.sh` (for an input in the repository) or `local_env.sh` (for an external input); there is no need to change file paths in scripts individually.
* It is easy to produce a graph of the input-output flow of the repository as a whole

## Documenting raw data

All raw input files (data, images, etc.) in the repository should be stored in the directory `0_raw`. The `README` file in that directory should provide detailed provenance for these files, including where, when, and how they were obtained. If the number of raw input files is large, `0_raw` may be divided into subdirectories, each of which may have its own `README` file. No modules downsream of `0_raw` should have any raw input files stored in them directly. The `/source/` directories of those downstream modules should only contain code.

The input files should in most cases be stored in exactly the form in which they were obtained. If a user wishes to do minimal pre-processing within the `0_raw` directory -- e.g., exporting data that was distributed as an Excel spreadsheet to CSV or restricting to a subset of records -- the truly raw data should be stored in  a `/0_raw/orig/` subdirectlry and the pre-processed data should be in `/0_raw/processed/`. The processing steps could happen by hand, in which case they should be documented in the `README`, or via code, in which case `0_raw` should have its own `make.sh` script and `/source/` subdirectory.

## Managing external input files

In some cases, a repository may depend on data files and other inputs that cannot be committed directly to Git -- e.g., because they are too large or because their license does not permit that. In this case, the local paths to these external dependencies can be defined as shell variables in `user_env.sh`. The `get_inputs.sh` scripts in the individual modules can then be updated to create symlinks to the external resources within `/input/`. The code can then refer to these files via their locations in `/input/` and remain agnostic about 

## Organizing with modules

Organizing a repository into modules has several advantages:

* The high-level structure of the repository is clear to the user
* Each module is a self-contained unit that a user can understand without looking at other modules
* Any given module can be run from beginning to end in a reasonable amount of time
* Well-organized modules produce clean commit histories

The default 4-module structure of the template is just an example. You should define and organize modules
in the way that makes sense for your projet. You can add additional modules at the top level of the repository --
for example,

* `1_data`
* `2_descriptive_analysis`
* `3_model_estimation`
* `4_slides`
* `5_paper`

Each of these subdirectories should have its own `make.sh`, `/source/`, and `/output/`.

You can also subdivide top-level subdirectories into multiple
modules -- for example,

* `1_data`
    - `1_survey_data`
    - `2_geo_data`
    - `3_admin_data`

In this case, each of `1_survey_data`, `2_geo_data`, and `3_admin_data` should have their own `make.sh`, `/source/`, and `/output/`.
The top-level `1_data` directory should not contain anything other than the subdirectories.

Here are some **key principles** for organizing modules:

* Use numerical prefixes like `1_xxx`, `2_xxx`, etc. to make clear the order in which modules should be run
* Each module should have a clear scope and purpose that a user can easily guess from its name
* Modules should be small enough that the `make.sh` script can be run in a reasonable amount of time. If a module takes hours or days to run, it is often a good idea to break it up into multiple smaller modules.
* Very slow steps should be isolated in separate modules. For example, if there is an estimation step that takes many days to run, this should be in a separate module from other steps like descriptive analysis, formatting tables and figures, etc.
* Steps that are modified and re-run frequently should be isolated in separate modules. For example, it often makes sense to separate formatting tables and figures from the analysis code that produces the inputs to the tables and figures.
* Modules should be defined to keep the dependency tree of the repository as simple and untangled as possible. For example, it is often a good sign if all downstream analysis modules call inputs from one or a small number of upstream data-building modules.

## Working with large data/input files

We find that it is a good idea to commit data/input files directly to Git whenever they are not too large. We use [Git LFS](https://git-lfs.com/) for this purpose, and we have had good experience for file sizes up to 10s of megabytes. Committing these files directly to Git means that the code and data are versioned together, that the results are guaranteed to be replicable, and that users do not have to deal with setting up and managing external dependencies.

For very large data or input files, however, committing to Git is inefficient at best. In this case, the inputs should be defined as external dependencies in `user_env.sh`. The comments in `user_env.sh` should provide detail on the nature of the external files, their provenance, and how a user can locate them. If the external files are raw data, they should be documented with a `README` just like the files in `0_raw`. If the external files are produced in a different repository, they should be called in a way that records the repository and revision that produced them. 

## Working with large output files

TBD

## Working with temporary or intermediate files

TBD

# FAQ

1. Question

   *Answer*

2. Question

   *Answer*
