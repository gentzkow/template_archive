clear all
set more off

program main
    import delimited "input/data.csv", clear
    replace x = x * 2
	export delimited "output/data_graph.csv", replace
end

* EXECUTE
main
