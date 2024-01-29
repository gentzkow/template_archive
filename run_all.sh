#!/bin/bash   
set -e

# Replace with name of your project
PROJECT_NAME="template"

# Tell user what we're doing
echo -e "Making \033[35m${PROJECT_NAME}\033[0m with shell: ${SHELL}"

# Run makeiles of each module
(cd 1_data && ${SHELL} make.sh)
(cd 2_analysis && ${SHELL} make.sh)
(cd 3_slides && ${SHELL} make.sh)
(cd 4_paper && ${SHELL} make.sh)
