* =============================================================================
* Short description of script's purpose
* =============================================================================

clear all
adopath + "../../lib/stata"

* =============================================================================

program main
    insheet using "../input/mpg.csv", comma clear
    clean_data
    save "../output/mpg.dta", replace
end

program clean_data
    di ""
    * Some data wrangling steps here
end

* Execute
main
