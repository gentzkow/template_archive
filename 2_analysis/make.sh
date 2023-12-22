#!/bin/bash   
set -e

# User-defined constants
MODULE_NAME=analysis
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
run_python analyze_data.py $LOGFILE
