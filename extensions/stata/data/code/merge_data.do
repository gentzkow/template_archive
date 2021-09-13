***************
* Environment *
***************

clear all
include input/lib/stata/standardize_env

program main
	import_chips
	import_tv
	merge_data
	export delim "output/temp/data_merged.csv", replace
end

program import_chips
	import delim using "input/chips.csv", clear
	save "output/temp/chips.dta"
end

program import_tv
	import delim using "input/tv.csv", clear
	save "output/temp/tv.dta"
end

program merge_data
	use "output/temp/chips.dta", clear
	merge m:1 county_id using "output/temp/tv.dta", assert(3) nogen
end

main
