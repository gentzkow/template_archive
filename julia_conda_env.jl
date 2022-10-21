#######################
### JULIA ENV SETUP ###
#######################

### Install Julia packages in the conda environment ###
### The default is to use the latest version of each of the Julia packages required.
### Comment the latest version of the package that was used in a full run. 

using Pkg

Pkg.add("DataFrames") #v1.4.1
Pkg.add("CSV") #v0.10.4
Pkg.add("StatsPlots") #v0.15.4
Pkg.add("Plots") #v1.35.5
Pkg.add("GR") #v0.69.5

# Check the version of the Julia packages
Pkg.status()