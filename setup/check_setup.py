#!/usr/bin/python

# ENVIRONMENT
import os
import imp
import shutil
import subprocess

try:
    import git 
    import yaml
    from termcolor import colored
    import colorama
    colorama.init()
except:
    print("Please pip install 'requirements.txt'")
    raise Exception

ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir
f, path, desc = imp.find_module('gslab_make', [os.path.join(ROOT, 'lib')])
gs = imp.load_module('gslab_make', f, path, desc)

default_executables = gs.private.metadata.default_executables
format_message = gs.private.utility.format_message


# GENERAL FUNCTIONS
def parse_yaml_files(config = '../config.yaml', config_user = '../config_user.yaml'):
    if not os.path.isfile(config_user):
        shutil.copy('config_user_template.yaml', config_user)

    config = yaml.load(open(config, 'rb'))
    config_user = yaml.load(open(config_user, 'rb'))

    return(config, config_user)


def check_executable(executable):
    if os.name == 'posix':
        try:
            subprocess.check_output('which %s' % executable, shell = True)
        except:
            error_message = "Please set up '%s' for command-line use on your system" % executable
            error_message = format_message(error_message)
            raise gs.private.exceptionclasses.ColoredError(error_message)
    if os.name == 'nt':
        try:
            subprocess.check_output('where %s' % executable, shell = True)
        except:
            try:
                subprocess.check_output('dir %s' % executable, shell = True)
            except:
                error_message = "Please set up `%s` for command-line use on your system" % executable
                error_message = format_message(error_message)
                raise gs.private.exceptionclasses.ColoredError(error_message, '')
       

def check_software(config, config_user):
    default_executables[os.name].update(config_user['local']['executables'])
    
    if config['git_lfs_required']:
        check_executable(default_executables[os.name]['git-lfs'])

    software_list = config['software_required']
    software_list = {key:value for (key, value) in software_list.items() if value == True}
    software_list = {key:default_executables[os.name][key] for (key, value) in software_list.items()}

    for software in software_list.values():
        check_executable(software)


def check_external_paths(config_user):
    if config_user['external']:
        for path in config_user['external'].values():
            if not os.path.exists(path):
                error_message = 'ERROR! Path `%s` listed in `config_user.yaml` but cannot be found.' % path
                error_message = format_message(error_message)
                raise gs.private.exceptionclasses.ColoredError(error_message)


def configuration():
    (config, config_user) = parse_yaml_files()
    check_software(config, config_user)
    check_external_paths(config_user)
    message = format_message('SUCCESS! Setup complete.')
    print(colored(message, 'green'))


# EXECUTE
configuration()