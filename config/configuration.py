#!/usr/bin/python

# ENVIRONMENT
import os
import shutil
import subprocess

# PYTHON
def check_executable(executable):
    try:
        subprocess.check_output(['which', executable])
    except:
        error_message = "Please set up '%s' for command-line use on your machine" % executable
        raise Exception('\n' + '*'*80 + '\n' + error_message + '\n' + '*'*80)

check_executable('pip')
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

import gslab_make as gs
import yaml

# GENERAL
def parse_yaml_files(config = 'config.yaml', config_user = '../config_user.yaml'):
    if not os.path.isfile(config_user):
        shutil.copy('config_user_template.yaml', config_user)

    config = yaml.load(open(config, 'rb'))
    config_user = yaml.load(open(config_user, 'rb'))

    gs.private.metadata.default_executables[os.name].update(config_user['local']['executables'])

    return(config, config_user)

def check_software(config, config_user):
    if config['git_lfs_required']:
        check_executable('git-lfs')

    software_list = config['software_required']
    software_list = {key:value for (key, value) in software_list.items() if value == True}
    software_list = {key:config_user['local']['executables'][key] for (key, value) in software_list.items()}

    for software in config_user['local']['executables'].values():
        check_executable(software)

def install_dependencies():
    PATHS = {'makelog': None}
    gs.run_r(PATHS, program = 'config_r.R')
    gs.run_stata(PATHS, program = 'config_stata.do')
    
def check_external_paths(config_user):
    for path in config_user['external'].values():
        if not os.path.isfile(path):
            print('*'*80 + '\nMissing file: %s\n' % path + '*'*80)

def configuration():
    (config, config_user) = parse_yaml_files()
    check_software(config, config_user)
    install_dependencies()
    check_external_paths(config_user)

configuration()