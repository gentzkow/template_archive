program main

end

program import_data
	import delim using "input/data_cleaned.csv", clear
	gen post_tv = (year > year_tv_introduced)
end

program run_regression
	areg chips_sold post_tv i.year, absorb(county_id)
	esttab
