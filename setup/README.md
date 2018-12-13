# Setup

## Instructions
1. Initialize `gslab_make` submodule using git
   ```
   git submodule deinit --all -f
   git submodule update --init --remote
   ```

2. Install Python dependencies listed in `requirements.txt` using pip
   ```
   pip install --user -r requirements.txt
   ```

3. Run `setup_repository.py`
   ```
   python setup_repository.py
   ```

4. Install Stata dependencies using `setup_stata.do`
   ```
   stata-mp -e setup_stata.do
   ```

5. Install R dependencies using `setup_r.r`
   ```
   Rscript setup_r.r
   ```


 
## FAQ

1. Help! I'm running into permission errors when trying to install Python dependencies!

<br>

![https://imgs.xkcd.com/comics/python_environment_2x.png](https://imgs.xkcd.com/comics/python_environment_2x.png){:height="50%" width="50%"}

<br>

```
pip install --user -r requirements.txt
```

```
sudo pip install -r requirements.txt
```

If you are using Anaconda, we recommend the following:
```
conda install --file requirements.txt"
```