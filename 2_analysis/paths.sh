# Absolute path to repository root
ROOT=$(readlink -f "..")
export ROOT

# Absolute path to output directory
OUTPUT=$(readlink -f "./output")
export OUTPUT

# Input paths
INPUT_DATA=${ROOT}/1_data/output/
export INPUT_DATA
