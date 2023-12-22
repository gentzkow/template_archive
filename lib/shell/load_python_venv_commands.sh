#!/bin/bash

# accepts an optional argument for the environment directory name
unset create_activate_venv
create_activate_venv() {

    # Define the environment directory
    if [ -z "$1" ]; then
        ENV_DIR="${PATH_TO_ROOT}/venv"
    else
        ENV_DIR="${PATH_TO_ROOT}/$1"
    fi

    # Create the virtual environment if it doesn't exist
    echo "Creating virtual environment: ${ENV_DIR}"
    if [ ! -d "$ENV_DIR" ]; then
        python -m venv $ENV_DIR
    fi

    # Activate the virtual environment
    echo "Activating virtual environment: ${ENV_DIR}"
    source $ENV_DIR/bin/activate

    # Install dependencies
    echo "Installing venv dependencies from setup/requirements.txt ..."
    pip install -r "${PATH_TO_ROOT}/setup/requirements.txt"

}

# accepts an optional argument for the environment directory name
unset activate_venv
activate_venv() {

    # Define the environment directory
    if [ -z "$1" ]; then
        ENV_DIR="${PATH_TO_ROOT}/venv"
    else
        ENV_DIR="${PATH_TO_ROOT}/$1"
    fi

    # Activate the virtual environment
    echo "Activating virtual environment: ${ENV_DIR}"
    source $ENV_DIR/bin/activate

}

