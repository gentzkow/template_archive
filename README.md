# README

## **Table of Contents**

 - [Requirements](#requirements)
 - [Setup](#setup)
 - [Running Package Scripts in Other Languages](#running-package-scripts-in-other-languages)
 - [Adding Packages](#adding-packages)
 - [Command Line Usage](#command-line-usage)
 - [User Configuration](#user-configuration)
 - [Windows Differences](#windows-differences)
 - [License](#license)

----
### Requirements

**_Note:_** The application requirements and setup instructions outlined below are intended to serve general users. To build the repository as-is, the following applications are required:

* [R](https://cran.r-project.org/mirrors.html)
* [Stata](https://www.stata.com/install-guide/)
* [Python](https://www.python.org/downloads/)
* [git](https://git-scm.com/download/mac)
* [git lfs](https://git-lfs.github.com/)
* [LyX](https://www.lyx.org/Download)
* A TeX distribution for your local OS (for example, [MacTeX](https://www.tug.org/mactex/) for MacOS).

You may download the latest versions of each. By default, the **[Setup](#setup)** instructions below will assume their usage. Note that some of these applications must also be invocable from the command line. See the **[Command Line Usage](#command-line-usage)** section for details on how to set this up. Note that if you wish to run `Julia` scripts in your repository, you will additionally need to [install `Julia`](https://julialang.org/downloads/) and set up its command line usage. Julia is currently not required to build the repository as-is. If you are planning to use a `conda` environment for development (see instructions below), you are not required to have local installations or enable command line usage of Stata, R, Python, or Julia (although this is recommended).

You must set up a personal `GitHub` account to [clone private repositories](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories) on which you are a collaborator. For public repositories (such as `template`), `Git` will suffice. You may need to set up [Homebrew](https://brew.sh/) if `git` and `git-lfs` are not available on your local computer.

If you are using MacOS, [ensure your terminal is operating in bash](https://www.howtogeek.com/444596/how-to-change-the-default-shell-to-bash-in-macos-catalina/) rather than the default `zsh`. MacOS users who are running `template` on an Apple Silicon chip will instead want to use `Rosetta` as their default terminal. You can find instructions on how to shift from `zsh` to `Rosetta` [here](https://osxdaily.com/2020/12/04/how-install-rosetta-2-apple-silicon-mac/) and [here](https://www.courier.com/blog/tips-and-tricks-to-setup-your-apple-m1-for-development/). 

WindowsOS users (with Version 10 or higher) will need to switch to `bash` from `PowerShell`. To do this, you can run `bash` from within a `PowerShell` terminal (you must have installed `git` first).

Once you have met these OS and application requirements, [clone a team repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) from `GitHub` and proceed to **[Setup](#setup)**.

----

### Setup

1. Create a `config_user.yaml` file in the root directory. An example can be found in the `/setup` directory. If this step is skipped, the default `config_user.yaml` will be copied over when running `check_setup.py` below. You might skip this step if you do not want not to specify any external paths, or want to use default executable names. See the **[User Configuration](#user-configuration)** section below for further details. 

2. Initialize `git lfs`. From the root of the repository, run:

```
   git lfs install
   ./setup/lfs_setup.sh
   git lfs pull
``` 

   This will not affect files that ship with the `template` (which use the standard `git` storage). The first command will initialize `git lfs` for usage. The second command will instruct `git lfs` to handle files with extensions such as `.pdf`, `.png`, etc. The third command will download large files from the remote repository to your local computer, if any exist. See [here](https://git-lfs.github.com/) for more  on how to modify your `git lfs` settings.

   Note that it is not required to initialize `git lfs` to work with the files hosted on `template`, but it is highly recommended that you initialize `git lfs` for large file storage by running the script above.

3. If you already have `conda` setup on your local machine, feel free to skip this step. If not, this will install a lightweight version of `conda` that will not interfere with your local `Python` and `R` installations.

  ***NOTE:*** If you do not wish to install `conda`, proceed to steps 6 - 8 (_installing `conda` is recommended_).

   Install [`miniconda`](https://docs.conda.io/en/latest/miniconda.html) to be used to manage the `R`/`Python` virtual environment, if you have not already done this. If you have `homebrew` (which can be download [here](https://brew.sh/)) `miniconda` can be installed as follows:

```
    brew install --cask miniconda
```

  Once you have installed `conda`, you need to initialize `conda` by running the following commands and *restarting your terminal*:

```
    conda config --set auto_activate_base false
    conda init $(echo $0 | cut -d'-' -f 2)
```

4. Next, create a `conda` environment with the commands:

```
    conda config --set channel_priority strict
    conda env create -f setup/conda_env.yaml
```

   By default, we recommend users to run `conda config --set channel_priority strict` to speed up conda building so that packages in lower priority channels are not considered if a package with the same name appears in a higher priority channel. However, if there is package version confilcts when building up, consider to remove strict `channel_priority` by running `conda config --set channel_priority flexible` becasue other channels might contain different version of packages with same name.

   The default name for the `conda` environment is `template`. This can be changed by editing the first line of `/setup/conda_env.yaml`. To activate the `conda` virtual environment, run:

```
    conda activate <project_name>
```

   The `conda` environment should be active throughout setup, and whenever executing modules within the project in the future. You can deactivate the environment with:

  ```
  conda deactivate <project_name>
  ``` 

_Please ensure that your `conda` installation is up to date before proceeding_. If you experience issues building your `conda` environment, check the version of your `conda` installation and update it if needed by running:

```
conda -V
conda update -n base -c defaults conda
```

Then, proceed to rebuild the environment.

5. Fetch `gslab_make` submodule files. We use a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to track our `gslab_make` dependency in the `/lib/gslab_make` folder. After cloning the repository, you will need to initialize and fetch files for the `gslab_make` submodule. One way to do this is to run the following `bash` commands from the root of the repository:

```
   git submodule init
   git submodule update
``` 

   Once these commands have run to completion, the `/lib/gslab_make` folder should be populated with `gslab_make`. For users with `miniconda`, proceed to step 7.

6. For users who do not want to install `miniconda`,  follow the instructions in `/setup/dependencies.md` to manually download all required dependencies. Ensure you download the correct versions of these packages. Proceed to step 7.

7. Run the script `/setup/check_setup.py`. One way to do this is to run the following `bash` command from the `/setup` directory (note that you _must_ be in the `/setup` directory, and you must have local installations of the softwares documented in **[Requirements](#requirements)**. for the script to run successfully):

```
   python check_setup.py
```

8. To build the repository, run the following `bash` command from the root of repository: 

   ```
   python run_all.py
   ```

----
### Adding Packages

_Note_: These instructions are relevant for users who have installed `miniconda`. If you have not done so, consult `/setup/dependencies.md`.

#### _Python_
Add any required packages to `/setup/conda_env.yaml`. If possible add the package version number as well. If there is a package that is not available from `conda`, add this to the `pip` section of the `yaml` file. In order to not re-run the entire environment setup you can download these individual files from `conda` with the command:

```
conda install -c conda-forge --name <environment name> <package_name=version_number>
```
#### _R_
Add any required packages that are available via `CRAN` to `/setup/conda_env.yaml`. These must be prepended with `r-`. If there is a package that is only available from `GitHub` and not from `CRAN`, add this package to `/setup/setup_r.r` (after copying this script from `/extensions`). These individual packages can be added in the same way as `Python` packages above (with the `r-` prepend). _Note that you may need to install the latest version of `conda` as outlined in the setup instructions above to properly load packages_.

#### _Stata_

Install `Stata` dependencies using `/setup/download_stata_ado.do` (copy `download_stata_ado.do` from `/extensions` to `/setup` first). We keep all non-base `Stata` ado files in the `lib` subdirectory, so most non-base `Stata` ado files will be versioned. To add additional `Stata` dependencies, use the following `bash` command from the `setup` subdirectory:

```
stata-mp -e download_stata_ado.do
```

#### _Julia_

First, add any required Julia packages to `julia_conda_env.jl`. Follow the same steps described in **[Setup](#setup)** to build and activate your `conda` environment, being sure to _uncomment the line referencing `julia` in `/setup/conda_env.yaml`_ before building the environment. Once the environment is activated, run the following line from the `/setup` directory:

```
julia julia_conda_env.jl
```

Then, ensure any Julia scripts are properly referenced in the relevant `make.py` scripts with the prefix `gs.run_julia`, and proceed to run `run_all.py`.

----

### Command Line Usage


For instructions on how to set up command line usage, refer to the [repo wiki](https://github.com/gentzkow/template/wiki/Command-Line-Usage).

By default, the repository assumes these executable names for the following applications:

```
application : executable

python      : python
git-lfs     : git-lfs
lyx         : lyx
r           : Rscript
stata       : stata-mp (this will need to be updated if using a version of Stata that is not Stata-MP)
julia       : julia
```

Default executable names can be updated in `config_user.yaml`. For further details, see the **[User Configuration](#user-configuration)** section.

----

### User Configuration
`config_user.yaml` contains settings and metadata such as local paths that are specific to an individual user and should not be committed to `Git`. For this repository, this includes local paths to [external dependencies](https://github.com/gentzkow/template/wiki/External-Dependencies) as well as executable names for locally installed software.

Required applications may be set up for command line usage on your computer with a different executable name from the default. If so, specify the correct executable name in `config_user.yaml`. This configuration step is explained further in the [repo wiki](https://github.com/gentzkow/template/wiki/Repository-Structure#Configuration-Files).

----


### Running Package Scripts in Other Languages
By default, this `template` is set up to run `Python` scripts. The `template` is, however, capable of running scripts in other languages too (make-scripts are always in `Python`, but module scripts called by make-scripts can be in other languages). 

  The directory `/extensions` includes the code necessary to run the repo with `R` and `Stata` scripts. Only code that differs from the default implementation is included. For example, to run the repo using `Stata` scripts, the following steps need to be taken. 
1. Replace `/analysis/make.py` with `/extensions/stata/analysis/make.py` and `/data/make.py` with `/extensions/stata/data/make.py`.
2. Copy contents of `/extensions/stata/analysis/code` to `/analysis/code` and contents of `/extensions/stata/data/code` to `/data/code`.
3. Copy `.ado` dependencies from `/extensions/stata/lib/stata` to `/lib/stata`. Included are utilities from the repo [`gslab_stata`](https://github.com/gslab-econ/gslab_stata).
4. Copy setup script from `/extensions/stata/setup` to `/setup`.

----

### Windows Differences

The instructions in `template` are applicable to Linux and Mac users. However, with just a few tweaks, this repo can also work on Windows.

If you are using Windows, you may need to run certain `bash` commands in administrator mode due to permission errors. To do so, open your terminal by right clicking and selecting `Run as administrator`. To set administrator mode on permanently, refer to the [repo wiki](https://github.com/gentzkow/template/wiki/Repository-Usage#Administrator-Mode).

The executable names are likely to differ on your computer if you are using Windows. Executable names for Windows generally resemble:

```
application : executable
python      : python
git-lfs     : git-lfs
lyx         : LyX#.# (where #.# refers to the version number)
r           : Rscript
stata       : StataMP-64 (will need to be updated if using a version of Stata that is not Stata-MP or 64-bit)
julia       : julia
```

To download additional `ado` files on Windows, you will likely have to adjust this `bash` command:

```
stata_executable -e download_stata_ado.do
```

`stata_executable` refers to the name of your `Stata` executable. For example, if your Stata executable was located in `C:\Program Files\Stata15\StataMP-64.exe`, you would want to use the following `bash` command:


```
StataMP-64 -e download_stata_ado.do
```

---

### License
MIT License

Copyright (c) 2019 Matthew Gentzkow

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

