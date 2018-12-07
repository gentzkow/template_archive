# Configuration

## Instructions
1. Install Python dependencies listed in `requirements.txt` using pip
   ```
   pip install --user -r requirements.txt
   ```

2. Run `configuration.py`
   ```
   python configuration.py
   ```

3. Install Stata dependencies using `config_stata.do`
   ```
   stata-mp -e config_stata.do
   ```

4. Install R dependencies using `config_r.r`
   ```
   Rscript config_r.r
   ```


 
## FAQ

1. Help! I'm running into 

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