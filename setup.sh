#!/bin/bash   

# Constants
PATH_TO_ROOT=.
ENV_DIR="lib/venv"
PATH_TO_CONFIG=${PATH_TO_ROOT}/lib/shmake/commands.sh

# load the shell utility library
source ${PATH_TO_CONFIG}

# create the virtual environment if it doesn't exist
# activate the virtual environment
if [ ! -d "$PATH_TO_ROOT/$ENV_DIR" ]; then
    echo "No virtual environment exists here: $PATH_TO_ROOT/$ENV_DIR"
    create_activate_venv "$PATH_TO_ROOT/$ENV_DIR"
else 
    echo "Virtual environment exists here: $PATH_TO_ROOT/$ENV_DIR"
    activate_venv "$PATH_TO_ROOT/$ENV_DIR"
fi
