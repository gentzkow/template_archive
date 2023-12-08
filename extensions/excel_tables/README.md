# README

---
## Purpose and Usage
---

This directory includes code which can be used to construct and export table objects in `gentzkow/template` from an Excel format to publication-ready PDF outputs. Note that the contents of this directory are intended to serve as a minimal working example of the functionality of the core function underlying the conversion: `export_excel_tables()` in the `run_program.py` script in the `gslab_make` submodule.

The structure of subdirectories in `/extensions/excel_tables/` parallels that of the overall repository. Files in each submodule directory (e.g. `/extensions/excel_tables/analysis/` or `/extensions/excel_tables/paper_slides/`) should be copied to the main submodule directory (e.g. `~/analysis/` or `~/paper_slides/`). 

Then executing make-scripts, for example with `python run_all.py`, will build outputs using the updated submodules from this `/extensions/` folder, rather than in the root directory.

---
## Procedure and Instructions
---

The procedure for constructing and exporting the Excel tables to PDF formats is documented below:

**(1)** The user computes matrices of numbers or scalars which they intend to present in a paper table. These calculations should compile within `~/analysis/` (in this minimal working example, in the script `/extensions/analysis/code/gen_scalars.R`).

Our working example constructs the scalars for Table 1 in the paper: [Pricing Power in Advertising Markets: Theory and Evidence](https://scholar.harvard.edu/files/shapiro/files/ad-price-drivers.pdf) (2022) by Matthew Gentzkow, Jesse M. Shapiro, Frank Yang, and Ali Yurukoglu.

These scalars should be stored in an `.xlsx` file format, as a matrix with any desired dimension. In this working example, the scalars are stored in the spreadsheet `/extensions/analysis/output/gs_primary_scalars.xlsx`.

**(2)** The user constructs the intended format (skeleton) of a production-ready table in Excel. In this minimal working example, this corresponds to the Excel sheet `/extensions/paper_slides/tables/skeletons/gs_primary.xlsx`.

Each of these skeleton tables should be stored in an `.xlsx` file format with *two separate sheets*.

- The first sheet will store imports of the matrices of numbers built in step (1) from `/extensions/analysis/output/`.
- The second sheet will store the skeleton of the table, with the desired formatting.

We use [spreadsheet linking](https://blog.coupler.io/how-to-link-excel-files/) to map scalar values in the first sheet (which will eventually populate with computed scalars from **(1)**) to their correct placements in the skeleton stored in the second sheet. Users should modify the formulas linking cells in the first sheet to cells in the second sheet depending on the features of their matrix compiled in `/extensions/analysis/output/` and the desired format of their skeleton in `/extensions/excel_tables/paper_slides/tables/skeletons`.

**(3)** The function which populates the scalars from `/extensions/analysis/output/` to `/extensions/analysis/paper_slides/skeletons` and exports the populated spreadsheet to a PDF format is called in `/extensions/paper_slides/make.py`.

The function requires two key arguments: the name of the skeleton table (in this example, `gs_primary`) and the name of the scalar export (in this example, `gs_primary_scalars`). The resulting PDF output from this minimal working example is stored in `/extensions/excel_tables/paper_slides/output/`

**(4)** Below are some additional notes on the function's usage, including call structure, file locations, file permissions, and export preferences:

- Each skeleton table requires a distinct call to this function, mapping the skeleton to the associated scalar output file.
- The function assumes the files are stored in `~/paper_slides/tables/skeletons/` and `~/paper_slides/input/`, respectively, and further requires that both files are saved with the `.xlsx` file format.
- When this function is called, the Excel program will automatically open on the user's application to attempt the export. Mac users will be required to allow the Excel software with access to the relevant files to enable these automated exports. Alternatively, users can grant the Excel software with disk access, by completing the setps below (one time on their local machine):

        (1) Open System Preferences.
        (2) Select Security & Privacy.
        (3) Go to the Privacy tab.
        (4) Scroll down the list to Files and Folders.
        (5) Click on the padlock and enter your password to allow changes.
        (6) Add Excel to the list of apps allowed to access Files and Folders.

- Optionally, the user can specify the additional argument `export = False`. In this case, when the function is run, the scalars will be properly populated, but the populated Excel sheets will not be automatically exported to a trimmed PDF format. To manually export the resulting Excel sheet to a PDF format, follow the instructions documented [here](https://blog.golayer.io/excel/how-to-convert-excel-to-pdf).
