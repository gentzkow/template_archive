#!/bin/bash   

source ${LIB}/utilities.sh

unset run_stata
run_stata() {

    if [[ $# -eq 3 ]]
    then 
        # get arguments
        stata_cmd="$1"
        program="$2"
        logfile="$3"

        # get path to file and file name
        local path_to_file=$(parse_fp "${program}" 3)
        local filename=$(parse_fp "${program}" 4)

        # run program
        (${stata_cmd} -e do ${program})

        # add default log to log file
        cat "${filename}.log" >> "${logfile}"
        # delete default log
        rm "${filename}.log"

    elif [[ $# -eq 2 ]]
    then
        # get arguments
        stata_cmd="$1"
        program="$2"

        # run stata (log file handled elsewhere)
        (${stata_cmd} -e do ${program})

    else 
        echo "ERROR IN RUN STATA: INVALID NUMBER OF ARGS"
    fi

}
