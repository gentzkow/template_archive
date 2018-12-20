# README

## Setup
1. Install Python dependencies listed in `requirements.txt` using pip. One way to do this is to use the following bash command from the `setup` subdirectory:
   
   ```
   pip install --user -r requirements.txt
   ```

2. Run `setup_repository.py`. One way to do this is to use the following bash command from the `setup` subdirectory:
   ```
   python setup_repository.py
   ```

3. Install Stata dependencies using `setup_stata.do`. One way to do this is to use the following bash command from the `setup` subdirectory:
   ```
   stata-mp -e setup_stata.do
   ```

4. Install R dependencies using `setup_r.r`. One way to do this is to use the following bash command from the `setup` subdirector:y
   ```
   Rscript setup_r.r
   ```
 
## FAQ

1. Help! I'm running into permission errors when trying to install Python dependencies!

<br>

![https://imgs.xkcd.com/comics/python_environment_2x.png](https://imgs.xkcd.com/comics/python_environment_2x.png){:height="50%" width="50%"}

<br>

The standard bash command for pip installing `requirements.txt` often runs into issues as depending on your Python environment, pip will attempt to install to a root directory (i.e., a directory that by default you should not have write permission)
```
pip install -r requirements.txtt
```

One way to get around this is to include `sudo` (or the Windows equivalent) in your bash command.
```
sudo pip install -r requirements.tx
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
   
   * If this is a directory that you should have write permission to but do not, use the `sudo chown` bash command (or the Windows equivalent) to get ownership.

   * If this is a directory that you should not have write permission to, change your `PYTHONUSERBASE` environment variable to a diretory that you should and do have write permission to.

If you are using Anaconda, we recommend using the following bash command:
```
conda install --file requirements.txt"
```
Note that you may run into issues if any of the Python depencencies are not available on the conda channels. If this is the case, revert back to using `pip`.