import subprocess
import pkg_resources
try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

pip_check = subprocess.check_output(['which', 'pip'])
if not pip_check:
    print("Please set up pip for command-line use on your machine")
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add required packages to this list
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
packages = ['pyyaml', 'numpy', 'matplotlib']
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(packages, upgrade):
    # Install gslab_make using pip
    pipmain(['install', '--upgrade', 'git+ssh://git@github.com/gentzkow/gslab_make.git@issue10_implement'])

    # Install required packages using pip
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]

    for pkg in packages:
        if upgrade:
            pipmain(['install', '--upgrade', pkg])
        elif pkg not in installed_packages:
            pipmain(['install', pkg])

# upgrade = TRUE will update all packages to the most current version
# upgrade = FALSE will skip packages that are already installed
main(packages, upgrade = False)


""" NOTES
(1)
As of pip 10, all internal APIs are no longer available. Functions in the `pip` namespace have been moved to `pip._internal`.
See [here](https://mail.python.org/pipermail/distutils-sig/2017-October/031642.html) for more detail.
Given this, we may want to switch the pip installations to subprocess calls:
```
subprocess.call(['pip', 'install', '--upgrade', pkg])
```

(2)
As of pip 10, uninstallation of distutils packages is no longer supported.
Potential (hacky) solutions include:

* Downgrading to pip 9
* Using the `--ignore-installed` flag

(3)
Potentially consider switching to using `requirements.txt` as well.
"""
