#!/usr/bin/python

# ENVIRONMENT
import os
import shutil
import subprocess
import gslab_make as gs
try:
    import yaml
except:
    print("Please pip install 'requirements.txt'")
    raise Exception

# GENERAL
def parse_yaml_files(config = '../config.yaml', config_user = '../config_user.yaml'):
    if not os.path.isfile(config_user):
        shutil.copy('config_user_template.yaml', config_user)

    config = yaml.load(open(config, 'rb'))
    config_user = yaml.load(open(config_user, 'rb'))
    gs.private.metadata.default_executables[os.name].update(config_user['local']['executables'])

    return(config, config_user)

def check_executable(executable):
    try:
        subprocess.check_output(['which', executable])
    except:
        error_message = "Please set up '%s' for command-line use on your system" % executable
        raise Exception('\n' + '*'*80 + '\n' + error_message + '\n' + '*'*80)

def check_software(config, config_user):
    if config['git_lfs_required']:
        check_executable('git-lfs')

    software_list = config['software_required']
    software_list = {key:value for (key, value) in software_list.items() if value == True}
    software_list = {key:config_user['local']['executables'][key] for (key, value) in software_list.items()}

def check_external_paths(config_user):
    for path in config_user['external'].values():
        if not os.path.isfile(path):
            print('*'*80 + "\nFile listed in 'config_user.yaml' but cannot be found: %s\n" % path + '*'*80)

def configuration():
    (config, config_user) = parse_yaml_files()
    check_software(config, config_user)
    check_external_paths(config_user)

configuration()