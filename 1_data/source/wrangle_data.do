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


  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      18.0
___/   /   /___/   /   /___/       MP—Parallel Edition

 Statistics and Data Science       Copyright 1985-2023 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata
> .com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user 4-core , expiring 21 Jul 2024
Serial number: 501809310346
  Licensed to: Matthew Gentzkow
               Stanford University

Notes:
      1. Stata is running in batch mode.
      2. Unicode is supported; see help unicode_advice.
      3. More than 2 billion observations are allowed; see help
          obs_advice.
      4. Maximum number of variables is set to 5,000 but can be
          increased; see help set_maxvar.

. do StataMP 
file StataMP.do not found
r(601);
