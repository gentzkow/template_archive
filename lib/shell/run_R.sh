#!/bin/bash   

unset run_R
run_R () {

    # get arguments
    program="$1"
    logfile="$2"

    # run program, add output to logfile
    (Rscript ${program} >> "${logfile}")
}

