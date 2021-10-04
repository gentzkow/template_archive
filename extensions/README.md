# README

This directory includes code which can be used to convert `gentzkow/template` from running on Python to R or Stata. Make-scripts (e.g. `make.py` and `run_all.py`) are always in Python, but files called by these scripts can be written in other languages.

The structure of subdirectories (`/extensions/<LANGUAGE>`) parallels that of the overall repository. Files in each submodule directory (e.g. `/extensions/<LANGUAGE>/analysis`) should be copied to the main submodule directory (e.g. `/analysis`). Then executing make-scripts, for example with `python run_all.py`, will build outputs using `<LANGUAGE>` instead of the default Python.

See the main `README` for more information.
