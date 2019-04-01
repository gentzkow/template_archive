#!/usr/bin/python

# ENVIRONMENT
import os
import shutil
import subprocess
import imp
try:
    import git 
    import yaml
except:
    print("Please pip install 'requirements.txt'")
    raise Exception

ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir
f, path, desc = imp.find_module('gslab_make', [os.path.join(ROOT, 'lib')])
gs = imp.load_module('gslab_make', f, path, desc)

# GENERAL
def parse_yaml_files(config = '../config.yaml', config_user = '../config_user.yaml'):
    if not os.path.isfile(config_user):
        shutil.copy('config_user_template.yaml', config_user)

    config = yaml.load(open(config, 'rb'))
    config_user = yaml.load(open(config_user, 'rb'))
    gs.private.metadata.default_executables[os.name].update(config_user['local']['executables'])

    return(config, config_user)

def check_executable(executable):
    if os.name == 'posix':
        try:
            subprocess.check_output(['which', executable])
        except:
            error_message = "Please set up '%s' for command-line use on your system" % executable
            raise Exception('\n' + '*'*80 + '\n' + error_message + '\n' + '*'*80)
    if os.name == 'nt':
        try:
            process = subprocess.Popen(['where', executable], 
                                       stdout = subprocess.PIPE, 
                                       stderr = subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                raise
        except:
            try:
                subprocess.check_output('dir %s' % executable, shell = True)
            except:
                error_message = "Please set up '%s' for command-line use on your system" % executable
                raise Exception('\n' + '*'*80 + '\n' + error_message + '\n' + '*'*80)
                       
def check_software(config, config_user):
    if config['git_lfs_required']:
        check_executable('git-lfs')

    software_list = config['software_required']
    software_list = {key:value for (key, value) in software_list.items() if value == True}

    for key in software_list.keys():
        try:
            software_list[key] = config_user['local']['executables'][key]
        except:
            software_list[key] = gs.private.metadata.default_executables[os.name][key] 

    for software in software_list.values():
        check_executable(software)

def check_external_paths(config_user):
    if config_user['external']:
        for path in config_user['external'].values():
            if not os.path.exists(path):
                print('*'*80 + "\nPath listed in 'config_user.yaml' but cannot be found: %s\n" % path + '*'*80)

def configuration():
    (config, config_user) = parse_yaml_files()
    check_software(config, config_user)
    check_external_paths(config_user)
    print('*'*80 + 'Setup complete' + '*'*80)

configuration()