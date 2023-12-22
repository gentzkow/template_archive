#!/bin/bash   
set -e

# User-defined constants
REPO_ROOT=..
LIB=${REPO_ROOT}/lib/shell
LOGFILE=output/make.log

# Load local environment and shell commands
source ${REPO_ROOT}/local_env.sh
source ${LIB}/run_python.sh
source ${LIB}/run_stata.sh
source ${LIB}/run_R.sh

# Remove previous output
rm -rf output
rm -f ${LOGFILE}
mkdir -p output

# Tell user what we're doing
MODULE=$(basename "$PWD")
echo "\n\nMaking \033[35m${MODULE}\033[0m module with shell: ${SHELL}"

# Run programs in order
(
	cd source 
	run_python analyze_data.py ../$LOGFILE
) 2>&1 | tee ${LOGFILE}

