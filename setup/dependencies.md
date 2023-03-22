# Installing Dependencies for Non-Conda Users (Locally and on Sherlock)

This file provides a set of instructions for users who are attempting to replicate a GS-Lab project, but do not wish to install `conda` on their local computers.

1. First, navigate to `setup/conda_env.yaml`. All of the required modules and versions
will be listed, for both `Python` and (when applicable) `R`.

2. You will need to install ALL of these packages (specifying the correct version) on
your local computer. To do so, you can either directly install packages on your local
software IDE (i.e., `PyCharm`, `Jupyter`, `RStudio`, etc.) OR install packages through your terminal. If you take the latter approach, you will want to run: `pip install <package==version_number>` and `Rscript -e "install.packages('<package=version_number>', repos = 'https://cloud/r-project.org')"`, for `Python` and `R` respectively. Note you will need to install `pip` (i.e., from Homebrew), and check that your `Python` and `R` applications match those in dependencies.

3. Once you have installed all required dependencies from `setup/conda_env.yaml`, proceed to
run `check_setup.py` from the `/setup` folder in the repository. You will be notified with a
warning message if any of the dependencies do not match.

_For users who are working with `Julia` scripts_:

Any `Julia` packages required for installation should be added to `julia_conda_env.jl`, rather than `setup/conda_env.yaml`. Regardless of whether a `conda` environment is active or not, _all users_ will need to
run `julia julia_conda_env.jl` from the root of their repository to install any relevant `Julia` packages from the [`Julia Pkg` package manager](https://juliapackages.com/). Users with an active `conda` environment will install these packages _without touching their local `Julia` software_, and do not need to set up `Julia` for Command Line Usage within their environment. Users who prefer not to use `conda` will need to [download `Julia`](https://julialang.org/downloads/) to their local computers, and set up the software for [Command Line Usage](https://github.com/gentzkow/template/wiki/Command-Line-Usage). All package installations will be made on the local version of `Julia`.

_For users who are working in Sherlock_ (an HPC utilized internally by lab members):
Follow the same steps above to install dependencies from `setup/conda_env.yaml`,
but ensure you have first loaded in the relevant modules through Sherlock (i.e., `Python` and `R`).

Note that to install `Python` packages in Sherlock, you will instead need to run:
`pip3 install --user <package==version_number>`. Remember to first check that `pip` is loaded.

For `R`, you will need to run: `"install.packages('<package==version_number>', repos='http://cran.us.r-project.org')"` _after_ initializing an `R` session using `ml R/<version_number>`.
