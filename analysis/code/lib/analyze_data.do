program main
	import_data
end

program import_data
	import delim using "input/data_cleaned.csv", clear
	gen post_tv = (year > year_tv_introduced)
end

program run_regression
	areg chips_sold post_tv i.year, absorb(county_id)
end	
	
program format_model
	matrix rtable = r(table)
	matrix formatted = J(1, 3, .) 
	matrix formatted[1, 1] = rtable["b", "post_tv"]
	matrix formatted[1, 2] = rtable["se", "post_tv"]
    matrix formatted[1, 3] = rtable["pvalue", "post_tv"]

	matrix_to_txt, matrix(formatted) ///
		saving("output/output.txt") ///
        title(<tab:regression>) replace
