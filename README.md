# README

## Requirements
All requirements must be installed and set up for command line usage. For further detail, see the **Command Line Usage** section below.

We manage Python and R installations using conda or miniconda. 
To build the repository as-is, the following applications are additionally required:

* [git-lfs](https://git-lfs.github.com/)
* [LyX](https://www.lyx.org/Download)
* [R](https://cran.r-project.org/mirrors.html)
* [Stata](https://www.stata.com/install-guide/)

These software are used by the scripts contained in the repository. By default, the **Setup** and **Build** instructions below will assume their usage. These applications also must be invocable from the command line. See the **Command Line Usage** section below for details.

## Setup 

1. Create a `config_user.yaml` file in the root directory. A template can be found in the `/setup` directory. See the **User Configuration** section below for further detail. 

   If you wish to not specify any external paths and/or to use the default executable names, you can skip this step and the default `config_user.yaml` will be copied over in step 4.

2. Optionally run the script `/setup/lfs_setup.sh`. This will instruct `git lfs` to handle files with extensions such as `.pdf`, `.png`, etc. This will not affect files that ship with the template. See [here](https://git-lfs.github.com/) for more information about modifying your repository's `git lfs` settings. 

3. If you already have conda setup on your local machine, feel free to skip this step. If not, this will install a lightweight version of `conda` that will not interfere with your current `python` and `R` installations.

   Install `miniconda` and `jdk` to be used to manage the R/Python virtual environment, if you have not already done this. You can install these programs from their websites [here for miniconda](https://docs.conda.io/en/latest/miniconda.html) and [here for jdk](https://www.oracle.com/java/technologies/javase-downloads.html). If you use homebrew (which can be download [here](https://brew.sh/)) these two programs can be downloaded as follows:
      ```
      brew install --cask miniconda
      brew install --cask oracle-jdk
      ```
   Once you have done this you need to initialize `conda` by running the following lines and restarting your terminal:
      ```
      conda config --set auto_activate_base false
      conda init $(echo $0 | cut -d'-' -f 2)
      ```

4. Create conda environment with the command:
      ```
      conda env create -f setup/conda_env.yaml
      ```
   The default name for the conda environment is `template`. This can be changed by editing the first line of `/setup/conda_env.yaml`. To activate the conda virtual environment just created, run
      ```
      conda activate PROJECT_NAME
      ```
   The environment should be active throughout setup, and whenver executing modules within the project in the future. You can deactivate the `conda` environment with
      ```
      conda deactivate
      ```

5. Fetch `gslab_make` submodule files. We use a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to track our `gslab_make` dependency in the `/lib/gslab_make` folder. After cloning the repository, you will need to initialize and fetch files for the `gslab_make` submodule. One way to do this is to run the following bash commands from the root of the repository:
   ```
   git submodule init
   git submodule update
   ``` 
   Once these commands have run to completion, the `/lib/gslab_make` folder should be populated with `gslab_make` files.   

6. Run the `/setup/check_setup.py` file. One way to do this is to run the following bash command in a terminal from the `/setup` subdirectory:
   ```
   python3 check_setup.py
   ```

## Running Package Scripts in Other Languages
By default, this template is set up to run python scripts. The template is, however, capable of running scripts in other languages too (make-scripts are always in python, but module scripts called by make-scripts can be in other languages). 

The directory `/extensions` includes the code necessary to run the repo with R and Stata scripts. Only code that differs from the default implementation is included. For example, to run the repo using Stata scripts, the following steps need to be taken. 
1. Replace `/analysis/make.py` with `/extensions/stata/analysis/make.py` and `/data/make.py` with `/extensions/stata/data/make.py`.
2. Copy contents of `/extensions/stata/analysis/code` to `/analysis/code` and contents of `/extensions/stata/data/code` to `/data/code`.
3. Copy `.ado` dependencies from `/extensions/stata/lib/stata` to `/lib/stata`. Included are utilities from the repo [`gslab_stata`](https://github.com/gslab-econ/gslab_stata).
4. Copy setup script from `/extensions/stata/setup` to `/setup`. More on the functionality of this script in the next section.

## Adding Packages
### Python
Add any required packages to `/setup/conda_env.yaml`. If possible add the package version number. If there is a package that is not available from `conda` add this to the `pip` section of the `yaml` file. In order to not re-run the entire environment setup you can download these individual files from `conda` with the command

```
conda install -c conda-forge <PACKAGE>
```

### R
Add any required packages that are available via CRAN to `/setup/conda_env.yaml`. These must be prepended with `r-`. If there is a package that is only available from GitHub and not from CRAN, add this package to `/setup/setup_r.r` (after copying this script from `/extensions`). These individual packages can be added in the same way as Python packages above (with the `r-` prepend).

### Stata

Install Stata dependencies using `/setup/download_stata_ado.do` (after copying this script from `/extensions`). We keep all non-base Stata ado files in the `lib` subdirectory, so most non-base Stata ado files will be versioned. To add additional stata dependencies, use the following bash command from the `setup` subdirectory:
```
stata-mp -e download_stata_ado.do
```

## Build

1. Follow the *Setup* instructions above.

2. From the root of repository, run the following bash command:
   ```
   python3 run_all.py
   ```

## Command Line Usage

For specific instructions on how to set up command line usage for an application, refer to the [repo wiki](https://github.com/gentzkow/template/wiki/Command-Line-Usage).

By default, the repository assumes the following executable names for the following applications:

```
application : executable
python      : python
git-lfs     : git-lfs
lyx         : lyx
r           : Rscript
stata       : stata-mp (will need to be updated if using a version of Stata that is not Stata-MP)
```

Default executable names can be updated in `config_user.yaml`. For further detail, see the **User Configuration** section below.

## User Configuration
`config_user.yaml` contains settings and metadata such as local paths that are specific to an individual user and thus should not be committed to Git. For this repository, this includes local paths to [external dependencies](https://github.com/gentzkow/template/wiki/External-Dependencies) as well as executable names for locally installed software.

Required applications may be set up for command line usage on your computer with a different executable name from the default. If so, specify the correct executable name in `config_user.yaml`. This configuration step is explained further in the [repo wiki](https://github.com/gentzkow/template/wiki/Repository-Structure#Configuration-Files).

## Windows Differences
The instructions above are for Linux and Mac users. However, with just a handful of small tweaks, this repo can also work on Windows. 

If you are using Windows, you may need to run certain bash commands in administrator mode due to permission errors. To do so, open your terminal by right clicking and selecting `Run as administrator`. To set administrator mode on permanently, refer to the [repo wiki](https://github.com/gentzkow/template/wiki/Repository-Usage#Administrator-Mode).

The executable names are likely to differ on your computer if you are using Windows. Executable names for Windows will typically look like the following:

```
application : executable
python      : python
git-lfs     : git-lfs
lyx         : LyX#.# (where #.# refers to the version number)
r           : Rscript
stata       : StataMP-64 (will need to be updated if using a version of Stata that is not Stata-MP or 64-bit)
```

To download additional `ado` files on Windows, you will likely have to adjust this bash command:
```
stata_executable -e download_stata_ado.do
```

`stata_executable` refers to the name of your Stata executable. For example, if your Stata executable was located in `C:\Program Files\Stata15\StataMP-64.exe`, you would want to use the following bash command:

```
StataMP-64 -e download_stata_ado.do
```
## License
MIT License

Copyright (c) 2019 Matthew Gentzkow

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
