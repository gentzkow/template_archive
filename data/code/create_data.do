version 14
set more off
preliminaries

set obs 300000
gen x = _n
export delimited "../output/data.txt", delimiter("|") replace
