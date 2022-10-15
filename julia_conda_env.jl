#######################
### JULIA ENV SETUP ###
#######################

# Set the path to the correct Python installation
ENV["PYTHON"]="/usr/local/Caskroom/miniconda/base/envs/template_julia/bin/python"

### Install Julia packages in the conda environment ###
### The default is to use the latest version of each of the Julia packages required.
### Comment the latest version of the package that was used in a full run. 

using Pkg
Pkg.add("Conda") # v1.4.1
Pkg.add("PyCall") # v1.4.1
Pkg.add("DataFrames") # v1.4.1
Pkg.add("CSV") # v0.10.4
Pkg.add("StatsPlots") # v0.15.4
Pkg.add("PyPlot") # v2.11.0

# Check the version of the Julia packages
#Use Pkg.status()