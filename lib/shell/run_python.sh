#!/bin/bash   

unset run_python
run_python () {

    # get arguments
    program="$1"
    logfile="$2"

    # set python command if unset
    if [ -z "$pythonCmd" ]; then
        echo "No python command set. Using default: python"
        pythonCmd="python"
    fi

    # run program, add output to logfile
    echo "Executing: ${pythonCmd} ${program} >> \"${logfile}\""
    (${pythonCmd} ${program} >> "${logfile}")
}
