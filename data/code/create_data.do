clear all
set more off

program main
    set obs 300000
    gen x = _n
    export delimited "output/data.txt", delimiter("|") replace
end

* EXECUTE
main
