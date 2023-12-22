#!/bin/bash   
set -e

# Project log
PROJECT_NAME="TunaTemplate"

# Print project name
echo -e "Making \033[35m${PROJECT_NAME}\033[0m with shell: ${SHELL}"

# Run makeiles of each module
(cd 1_data && ${SHELL} make.sh)
(cd 2_analysis && ${SHELL} make.sh)
(cd 3_paper_slides && ${SHELL} make.sh)
