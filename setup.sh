#!/bin/bash   

# Create local_env.sh if it does not exist. This is a configuration file
# that contains paths, executable names, and other settings specific to 
# a user's local machine. It file is ignored by Git so changes only affect
# the local copy of the repository.
if [ -f "local_env.sh" ]; then
    echo "Note: File local_env.sh already exists"
else
    cp lib/setup/local_env_template.sh local_env.sh
fi
