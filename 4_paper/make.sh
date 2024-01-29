#!/bin/bash   
set -e

# User-defined constants
REPO_ROOT=..
LIB=${REPO_ROOT}/lib/shell
LOGFILE=output/make.log

# Load local environment and shell commands
source ${REPO_ROOT}/local_env.sh
source ${LIB}/run_latex.sh

# Clear output directory
rm -rf output
rm -f ${LOGFILE}
mkdir -p output

# Copy and/or symlink inputs
rm -rf input
cp -r ${REPO_ROOT}/1_data/output input

# Tell user what we're doing
MODULE=$(basename "$PWD")
echo "\n\nMaking \033[35m${MODULE}\033[0m module with shell: ${SHELL}"

# Run programs in order
(
    cd source 
    run_latex my_project.tex ../$LOGFILE ../output
) 2>&1 | tee ${LOGFILE}
