#!/bin/bash   
set -e

# User-defined constants
MODULE_NAME=data
LOGFILE=output/build.log

# Load paths, local environment, and utilities
source paths.sh
source ${ROOT}/local_env.sh
source ${ROOT}/lib/shell/load_make_commands.sh

# remove previous output
rm -rf output
rm -f ${LOGFILE}
mkdir -p output

# print shell being used
echo "\n\nMaking \033[35m${MODULE_NAME}\033[0m module with shell: ${SHELL}"

# run programs in order
(
	cd source 
	run_python merge_data.py ../$LOGFILE 
	run_python clean_data.py ../$LOGFILE 
) 2>&1 | tee ${LOGFILE}