#!/usr/bin/python

import os
import shutil
import subprocess

# Check that gslab_make library is correctly installed 
# import config_python
import gslab_make as gs
import yaml

# Check that config_local.yaml exists; create it from template if it does not
# Check that config_local.yaml and config.yaml parse correctly
def parse_yaml_files(config_yaml = 'config.yaml', config_user_yaml = '../config_user.yaml'):
    if not os.path.isfile(config_user_yaml):
        shutil.copy('config_user_template.yaml', config_user_yaml)

    config_yaml = yaml.load(open(config_yaml, 'rb'))
    config_user_yaml = yaml.load(open(config_user_yaml, 'rb'))

    gs.private.metadata.default_executables[os.name].update(config_user_yaml['local']['executables'])

    return(config_user_yaml)

# Check that software packages are correctly installed
def check_software(config_user_yaml):
    for software in config_user_yaml['local']['executables'].values():
        check = subprocess.check_output(['which', software])
        if check:
            print(check)
        else:
            print("Missing following software: %s" % software)

# Install dependencies for Python, R, Stata
def install_dependencies():
    PATHS = {'makelog': None}
    gs.run_r(PATHS, program = 'config_r.R')
    gs.run_stata(PATHS, program = 'config_stata.do')
    
# Check that paths to all external resources are valid
def check_path(config_user_yaml):
    for path in config_user_yaml['external'].values():
        if not os.path.isfile(path):
            print("Missing file: %s" % path)

def configuration():
    config_user_yaml = parse_yaml_files()
    check_software(config_user_yaml)
    install_dependencies()
    check_path(config_user_yaml)

configuration()
