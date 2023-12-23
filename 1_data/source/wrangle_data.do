* =============================================================================
* Short description of script's purpose
* =============================================================================

clear all
adopath + "../../lib/stata"

* Paths
global input_dir "../../0_raw"
global output_dir "../output"

* =============================================================================

program main
    insheet using "$input_dir/mpg.csv", comma clear
    clean_data
    save "$output_dir/mpg.dta", replace
end

program clean_data
    di ""
    * Some data wrangling steps here
end

* Execute
main

