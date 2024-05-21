# README

---
## Purpose and Usage
---

This directory includes code which can be used to construct and export table objects in `gentzkow/template` from an Excel format (**input**) to publication-ready PDF tables (**output**).

The structure of subdirectories in `/extensions/excel_tables/` parallels that of the overall repository. Files in each submodule directory (e.g. `/extensions/excel_tables/analysis/` or `/extensions/excel_tables/paper_slides/`) should be copied to the main submodule directory (e.g. `~/analysis/` or `~/paper_slides/`).

---
## Procedure and Instructions
---

_For all users_: **Please note: this process will call Excel using your computer's native software. Be sure to save any open Excel sheets prior to running this code, as the application will exit and restart.**

_For users on Windows machines_: Please ensure you construct the `conda` environment with the `pywin32` package installed before proceeding (see `/setup/conda_env.yaml`).

The procedure for constructing and exporting the Excel tables to PDF formats is documented below:

**(1)** The user computes matrices of numbers or scalars which they intend to present in a paper table. These calculations should compile within `~/analysis/`. These scalars should be stored as a matrix in an `.xlsx` file format.

**(2)** The user constructs the intended format (skeleton) of a production-ready table in Excel. Each skeleton tables should be stored in an `.xlsx` file format with _two separate sheets_.

- The first sheet will store imports of the matrices of numbers built in step (1) from `/extensions/analysis/output/`.
- The second sheet will store the skeleton of the table, with the desired formatting.

**(3)** In `/extensions/paper_slides/make.py`, we call the function which **(a)** populates the scalars from `/extensions/analysis/output/` to `/extensions/analysis/paper_slides/skeletons`, and **(b)** exports the populated spreadsheet to a PDF format.

**(4)** Below are some additional notes on the function's usage, including call structure, file locations, file permissions, and export preferences:

- The function assumes the files are stored in `~/paper_slides/tables/skeletons/` and `~/paper_slides/input/`, respectively, and further requires that both files are saved with the `.xlsx` file format.
- When this function is called, the Excel program will automatically open on the user's application to attempt the export. Mac users will be required to allow the Excel software with access to the relevant files to enable these automated exports. Alternatively, users can grant the Excel software with disk access, by completing the setps below (one time on their local machine):

        (1) Open System Preferences.
        (2) Select Security & Privacy.
        (3) Go to the Privacy tab.
        (4) Scroll down the list to Files and Folders.
        (5) Click on the padlock and enter your password to allow changes.
        (6) Add Excel to the list of apps allowed to access Files and Folders.

- Optionally, the user can specify the additional argument `export = False`. In this case, when the function is run, the scalars will be properly populated, but the populated Excel sheets will not be automatically exported to a trimmed PDF format. To manually export the resulting Excel sheet to a PDF format, follow the instructions documented [here](https://blog.golayer.io/excel/how-to-convert-excel-to-pdf).
