#!/usr/bin/python

# ENVIRONMENT
import os
import importlib
import shutil
import subprocess
import sys

try:
    import yaml
    from termcolor import colored
    import colorama
    colorama.init()

except:
    print("Please ensure that conda env is activated and that yaml,")
    print("termcolor, and colorama are in conda_env.yaml")
    raise Exception

ROOT = '..'
# IMPORT GSLAB MAKE
gslm_path = os.path.join(ROOT, 'lib', 'gslab_make')
sys.path.append(gslm_path)
import gslab_make as gs

default_executables = gs.private.metadata.default_executables
format_message = gs.private.utility.format_message


# GENERAL FUNCTIONS
def read_env_yaml():
    with open('conda_env.yaml', 'r') as file:
        packages = yaml.safe_load(file)
    return packages


def get_python(packages):
    prefixes_python = ('python', 'python=', "pip=", "r=", "r-", "r", "pyyaml", "gitpython")
    python_packages = [item for item in packages['dependencies'] if not 
                       item.startswith(prefixes_python)]
    return python_packages


def get_r(packages):
    prefixes_r = ("r-")
    r_packages = [item for item in packages['dependencies'] if item.startswith(prefixes_r)] 
    return r_packages


def parse_yaml_files(config = '../config.yaml', config_user = '../config_user.yaml'):
    if not os.path.isfile(config_user):
        shutil.copy('config_user_template.yaml', config_user)

    config = yaml.load(open(config, 'rb'), Loader = yaml.Loader)
    config_user = yaml.load(open(config_user, 'rb'), Loader = yaml.Loader)

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


def check_dependencies():
    try:
        import importlib
        packages = read_env_yaml()
        python_packages = get_python(packages)
        r_packages = get_r(packages)
        for package in python_packages:
            globals()[package] = importlib.import_module(package)
        for package in r_packages:
            package = package.replace('r-',"")
            output=str(subprocess.run(['Rscript', '-e', f'library("{package}")']))
            if "returncode=0" not in output:
                error_message = 'ERROR! R package `%s` is not installed.' % package
                error_message = format_message(error_message)
                raise gs.private.exceptionclasses.ColoredError(error_message)
        if 'pyyaml' in python_packages:
            import yaml
        if 'gitpython' in python_packages:
            import git
            
    except:
        error_message = "Please ensure that you have the correct conda environment activated.\nIf you are not using conda, ensure you have installed all dependencies from ~/setup/dependencies.md."
        error_message = format_message(error_message)
        raise gs.private.exceptionclasses.ColoredError(error_message)
        raise Exception


def configuration():
    (config, config_user) = parse_yaml_files()
    check_software(config, config_user)
    check_external_paths(config_user)
    check_dependencies()
    message = format_message('SUCCESS! Setup complete.')
    print(colored(message, 'green'))


# EXECUTE
configuration()
