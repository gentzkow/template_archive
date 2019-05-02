# README

## Requirements
All requirements must be installed and setup for command line usage. For details on how to setup command line usage for an application, refer to the [RA manual](https://github.com/gentzkow/template/wiki/Command-Line-Usage).

* Python (2.7/3.7)
* pip (>=10.0)

To build the repository as-is, the following applications are additionally required:

* git-lfs
* LyX
* R
* Stata

These applications are used by the example scripts contained in the repository. By default, the **Setup** instructions below will assume their usage.

## Setup
**If you are using Windows, you will need to run all bash commands in administrator mode. To do so, open your terminal by right clicking and selecting `Run as administrator`.**

1. Create a `config_local.yaml` file in the root directory. A template can be found in the `setup` subdirectory. See the **Config** section below for further detail.

2. Install Python dependencies listed in the `requirements.txt` file using pip. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   python -m pip install --user -r requirements.txt
   ```

3. Run the `setup_repository.py` file. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   python setup_repository.py
   ```

4. Install Stata dependencies using the `setup_stata.do` file. One way to do this is to use the following bash command from the `setup` subdirectory:
   ```
   stata-mp -e setup_stata.do
   ```

   If you are using a Windows, you will likely have to adjust this bash command:
   ```
   stata_executable -e setup_stata.do
   ```

   `stata_executable` refers to the name of your Stata executable. For example, if your Stata executable was located in `C:\Program Files\Stata15\StataMP-64.exe`, you would want to use the following bash command:

   ```
   StataMP-64 -e setup_stata.do
   ```

5. Install R dependencies using the `setup_r.r` file. One way to do this is to run the following bash command in a terminal from the `setup` subdirectory:
   ```
   Rscript setup_r.r
   ```

## FAQ
1. Help! I'm running into permission errors when trying to install Python dependencies!

<br>

<img src="https://imgs.xkcd.com/comics/python_environment_2x.png" width="400" height="400">

<br>

The standard bash command for pip installing `requirements.txt` often runs into issues as depending on your Python environment, pip will attempt to install to a root directory (i.e., a directory that by default you should not have write permission)
```
python -m pip install -r requirements.txt
```

One way to get around this is to include `sudo` (or the Windows equivalent of running in administrative mode) in your bash command.
```
sudo python -m pip install -r requirements.txt
```

However, we caution against this given the potential security risks. Instead, we recommend including the `--user` flag to your bash command.
```
python -m pip install --user -r requirements.txt
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