# README

By default, the `template` repo runs data preparation and analysis code in Python. These tasks can be also accomplished in Stata, and the materials for doing so are contained in this directory.

The structure of this directory, `/extensions/stata` parallels that of the overall repository. Files in each submodule directory (e.g. `/extensions/stata/analysis`) should be copied to the main submodule directory (e.g. `/analysis`). Then executing make-scripts, for example with `python run_all.py`, will build outputs using Stata instead of the default Python.

See the main `README` for more information.
