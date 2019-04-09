# README

## Requirements
All requirements must be installed and setup for command line usage. For more details, see the **Command line usage** section. 

* Python (2.7/3.7)
* pip (>=10.0)

To build the repository as-is, the following applications are additionally required:

* git-lfs
* LyX
* R
* Stata

These applications are used by the example scripts contained in the repository. By default, the **Setup** instructions below will assume their usage.

## Command line usage

### Mac
To setup an application for command line usage, its executable must be added to **PATH** so that the OS can locate it. By default, the template assumes the following executable names for the following applications. 
   ```
   application : executable
   Python      : python
   pip         : pip
   git-lfs     : git-lfs
   LyX         : lyx
   R           : Rscript
   Stata       : statamp
   ```

While these are the typical executable names for Mac, it is possible that they may differ on your computer. Default executable names can be updated in `config_user.yaml`. See the **Config** section below for further detail.

To check if an application is setup for command line usage, type `which executable` into a terminal. If no path appears, then the application is not setup for command line usage. To add the executable of an application to **PATH**:

1. Locate the executable for an application. For example, the executable for Stata is typically found at `/Applications/Stata/StataMP.app/Contents/MacOS/statamp`.
2. In a terminal, from your user directory (`/Users/name`) run the following bash commands:

```
touch .bash_profile
nano .bash_profile
```

3. The [Nano editor](https://wiki.gentoo.org/wiki/Nano/Basics_Guide) should appear in your terminal. Type in the path to the executable into the Nano editor in the following format `PATH="$PATH:path_to_executable` where `path_to_executable` refers to the full path of the directory containing the executable. 

   For example, if your Stata executable was located in `/Applications/Stata/StataMP.app/Contents/MacOS/statamp`, you would want to type in the following text into the Nano editor: `PATH="$PATH:/Applications/Stata/StataMP.app/Contents/MacOS/`.

4. Save and exit the Nano editor by pressing CTRL + X, Y, and enter.

### Windows
To setup an application for command line usage, its executable must be added to **PATH** so that the OS can locate it. By default, the template assumes the following executable names for the following applications. 
```
application : executable
Python      : python
pip         : pip
git-lfs     : git-lfs
LyX         : lyx
R           : Rscript
Stata       : statamp
```

However, these are the default executable names for Mac and therefore likely to differ on your computer. Default executable names can be updated in `config_user.yaml`. See the **Config** section below for further detail. Executable names for Windows will typically look like the following:

```
application : executable
Python      : python
pip         : pip
git-lfs     : git-lfs
LyX         : LyX#.# (where #.# refers to the version number)
R           : Rscript
Stata       : path_to_stata_executable
```

`path_to_stata_executable` refers to full path of your Stata executable. For example, if your Stata executable was located in `C:\Program Files\Stata15\StataMP-64.exe`, you would want to type in the following into your `config_user.yaml`: `stata: '"C:\Program Files\Stata15\StataMP-64.exe"'` (note double quotes to accommodate spaces in the path). As long as you type in the full path of your Stata executable, there is no need to add it to **PATH**.

To check if an application is setup for command line usage, type `where executable` into a terminal. If no path appears, then the application is not setup for command line usage. To add the executable of an application to **PATH**:

1. Locate the executable for an application. For example, the executable for R might be found at `C:\Program Files\R\R-3.5.0\bin\x64\RScript.exe`.
2. In your start menu, search "environment". Click on `Edit the system environment variables`. 
3. Click on `Environment Variables`. You should see a panel that is labeled `User Variables`. In the panel, click on the variable called `Path`.
4. Click on `Edit`. Click on `New`.
5. Type in the full path of the directory containing the executable.

   For example, if your R executable was located in `C:\Program Files\R\R-3.5.0\bin\x64\RScript.exe`, you would want to type in the following text: `C:\Program Files\R\R-3.5.0\bin\x64\`

6. Click `OK`.

## Setup
**If you are using Windows, you will need to run all bash commands in administrator mode. To do so, open your terminal by right clicking and selecting `Run as administrator`.**

1. Create a `config_local.yaml` file in the root directory. A template can be found in the `setup` subdirectory. See the **Config** section below for further detail.

2. Install Python dependencies listed in the `requirements.txt` file using pip. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   pip install --user -r requirements.txt
   ```

3. Run the `setup_repository.py` file. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   python setup_repository.py
   ```

4. Install Stata dependencies using the `setup_stata.do` file. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   stata-mp -e setup_stata.do
   ```

   ```
   stata-mp -e setup_stata.do
   ```

5. Install R dependencies using the `setup_r.r` file. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   Rscript setup_r.r
   ```
 
## Build
**If you are using Windows, you will need to run all bash commands in administrator mode. To do so, open your terminal by right clicking and selecting `Run as administrator`.**

To build the repository as-is from start to finish, the following procedure should be implemented:

1. From the `data` subdirectory, run the following bash command in a terminal:
   ```
   python make.py
   ```

2. From the `analysis` subdirectory, run the following bash command in a terminal:
   ```
   python make.py
   ```

3. From the `paper_slides` subdirectory, run the following bash command in a terminal:
   ```
   python make.py
   ```

**If you are using Windows, you will need to run all bash commands in administrator mode. To do so, open your terminal by right clicking and selecting `Run as administrator`.**

## Config
`config.yaml` specifies the minimum required applications to initialize the repository. By default, this includes the following applications:

   - git-lfs
   - LyX
   - R
   - Stata

All required applications must be installed and setup for command line usage. If not, an error message will be raised when attempting to run `setup_repository.py`.

`config_user.yaml` specifies local settings for the user. This includes the following.

1. **External dependencies**: Any files external to the repository should be specified in `config_user.yaml`. Furthermore, any reference to external files in code should be made via an import of `config_user.yaml`.

    The following protocol for external dependencies should ideally be used:

    * Specify external dependencies in `config_user.yaml`.

    * Create symbolic links to external dependencies using `gslab_make.create_external_links`.

    * Reference external dependencies via symbolic links as opposed to actual path.

2. **Executable names**: Required applications may be setup for command line usage on your computer with a different executable name from the default. If so, specify the correct executable name in `config_user.yaml`

## FAQ
1. Help! I'm running into permission errors when trying to install Python dependencies!

<br>

<img src="https://imgs.xkcd.com/comics/python_environment_2x.png" width="400" height="400">

<br>

The standard bash command for pip installing `requirements.txt` often runs into issues as depending on your Python environment, pip will attempt to install to a root directory (i.e., a directory that by default you should not have write permission)
```
pip install -r requirements.txt
```

One way to get around this is to include `sudo` (or the Windows equivalent of running in administrative mode) in your bash command.
```
sudo pip install -r requirements.txt
```

However, we caution against this given the potential security risks. Instead, we recommend including the `--user` flag to your bash command.
```
pip install --user -r requirements.txt
```

The `--user` flag instructs pip to install to a local directory (i.e., a directory that by default you should have write permission). If you are still running into permission errors, we recommend the following diagnostic steps:

   * Find the local directory that pip is attempting to install to. You can do this by either looking at the permission error message or using the following bash commands:
   ```
   python
   import site
   site.USER_SITE
   ```
   
   * If this is a directory that you should have write permission to but do not, use the `sudo chown` bash command (or the Windows equivalent of changing ownership through properties) to get ownership.

   * If this is a directory that you should not have write permission to, change your `PYTHONUSERBASE` environment variable to a directory that you should and do have write permission to.

If you are using Anaconda, we recommend using the following bash command:
```
conda install --file requirements.txt"
```
Note that you may run into issues if any of the Python dependencies are not available on the conda channels. If this is the case, revert back to using `pip`.