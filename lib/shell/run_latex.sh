#!/bin/bash   

source ${LIB}/utilities.sh

unset run_latex
run_latex() {

    # Get arguments
    programname=$(basename "$1" .tex)
    logfile="$2"
    outputdir="$3"

    abslogfile=$(get_abs_filename "${logfile}")

    # Run program, add output to logfile
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
    pdflatex ${programname}.tex >> "${abslogfile}"
	for i in {1..10}; do echo >> "${abslogfile}"; done
    
    echo "Executing: bibtex ${programname}.aux >> \"${logfile}\""
    if (bibtex ${programname}.aux >> "${abslogfile}"); then
        echo "Successfully ran bibtex"
    else
        # Print error message
        echo "Error: bibtex failed. See ${logfile} for details."
    fi
	for i in {1..10}; do echo >> "${abslogfile}"; done
    
    echo "Sleeping 1 second..."
    sleep 1
    
    echo "Executing: pdflatex ${programname}.tex >> \"${logfile}\""
	pdflatex ${programname}.tex >> "${abslogfile}"
    for i in {1..10}; do echo >> "${abslogfile}"; done

    echo "Executing: pdflatex ${programname}.tex >> \"${logfile}\""
	pdflatex ${programname}.tex >> "${abslogfile}"
	for i in {1..10}; do echo >> "${abslogfile}"; done

    # Remove program artifacts
    rm -f ${programname}.toc
	rm -f ${programname}.apt
	rm -f ${programname}.aux
	rm -f ${programname}.lof
	rm -f ${programname}.lot
	rm -f ${programname}.log
	rm -f ${programname}.out
    rm -f ${programname}.bbl
    rm -f ${programname}.blg

    # Move PDF to output directory
    mv "${programname}.pdf" "${outputdir}"
}

