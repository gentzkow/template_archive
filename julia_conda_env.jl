#######################
### JULIA ENV SETUP ###
#######################

### Install Julia packages in the conda environment ###
### The default is to use the latest version of each of the Julia packages required.
### Comment the latest version of the package that was used in a full run. 

using Pkg
Pkg.add("Conda")
using Conda
Pkg.add(["PyCall", "DataFrames", "CSV", "StatsPlots", "PyPlot"])

# Check the version of the Julia packages
#Use Pkg.status()