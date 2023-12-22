#!/bin/bash   

# separates "./path/to/program.do" into
#   (1) file = program.do
#   (2) extension = do
#   (3) path_to_file = ./path/to/
#   (4) filename = program
unset parse_fp 
parse_fp() {

    # get arguments
    fp="$1"
    opt="$2"
    
    file="${fp##*/}"

    case $opt in
        1)  output="${file}"
            ;;
        2)  output="${file##*.}"
            ;;
        3)  output="${fp%"${file}"}"
            ;;
        4)  output="${file%.*}"
            ;;
        *)  output="ERROR in parse_fp: unmatched option"
            ;;
    esac

    echo "${output}"

}

unset get_abs_filename
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")"; pwd -P)/$(basename "$1")"
}

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

unset run_shell
run_shell() {

    # get arguments
    program="$1"
    logfile="$2"

    # run program, add output to logfile
    (${SHELL} ${program} >> "${logfile}")

}

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

unset run_R
run_R () {

    # get arguments
    program="$1"
    logfile="$2"

    # run program, add output to logfile
    (Rscript ${program} >> "${logfile}")
}

unset run_latex
run_latex() {

    # get arguments
    programname="$1"
    logfile="$2"

    abslogfile=$(get_abs_filename "${logfile}")

    # run program, add output to logfile
    rm -f ${programname}.toc
	rm -f ${programname}.apt
	rm -f ${programname}.aux
	rm -f ${programname}.lof
	rm -f ${programname}.lot
	rm -f ${programname}.log
	rm -f ${programname}.out
    rm -f ${programname}.bbl
    rm -f ${programname}.blg
	rm -f ${programname}.pdf
	rm -f missfont.log

    echo "Executing: pdflatex ${programname}.tex >> \"${logfile}\""
    (cd code && pdflatex ${programname}.tex >> "${abslogfile}")
	for i in {1..10}; do echo >> "${abslogfile}"; done
    
    echo "Executing: bibtex ${programname}.aux >> \"${logfile}\""
    if (cd code && bibtex ${programname}.aux >> "${abslogfile}"); then
        echo "Successfully ran bibtex"
    else
        # print error message
        echo "Error: bibtex failed. See ${logfile} for details."
    fi
	for i in {1..10}; do echo >> "${abslogfile}"; done
    
    echo "Sleeping 1 second..."
    sleep 1
    
    echo "Executing: pdflatex ${programname}.tex >> \"${logfile}\""
	(cd code && pdflatex ${programname}.tex >> "${abslogfile}")
    for i in {1..10}; do echo >> "${abslogfile}"; done

    echo "Executing: pdflatex ${programname}.tex >> \"${logfile}\""
	(cd code && pdflatex ${programname}.tex >> "${abslogfile}")
	for i in {1..10}; do echo >> "${abslogfile}"; done

    # remove program artifacts
    rm -f ${programname}.toc
	rm -f ${programname}.apt
	rm -f ${programname}.aux
	rm -f ${programname}.lof
	rm -f ${programname}.lot
	rm -f ${programname}.log
	rm -f ${programname}.out
    rm -f ${programname}.bbl
    rm -f ${programname}.blg

}

