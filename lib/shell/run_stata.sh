#!/bin/bash   

source ${LIB}/utilities.sh

unset run_stata
run_stata() {
    # get arguments
    program="$1"
    logfile="$2"
    
    # get path to file and file name
    local filename=$(parse_fp "${program}" 4)

    # set Stata command if unset
    if [ -z "$stataCmd" ]; then
        echo "No Stata command set. Using default: StataMP"
        stataCmd="StataMP"
    fi

    # run program, add output to logfile
    echo "Executing: ${stataCmd} ${program} >> \"${logfile}\""
    (${stataCmd} -e do ${program})

    # add default log to log file and then delete default log
    cat "${filename}.log" >> "${logfile}"
    rm "${filename}.log"
}
