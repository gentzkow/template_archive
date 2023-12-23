* =============================================================================
* Short description of script's purpose
* =============================================================================

clear all
adopath + "../../lib/stata"
set linesize 100

* Paths
global input_dir "../../1_data/output"
global output_dir "../output"

* =============================================================================

program main
    use "$input_dir/mpg.dta", clear
    regression_table
	city_figure
	hwy_figure
end

program regression_table
	reg displ cty
	estimates store cty
	
	reg displ hwy
	estimates store hwy
	
	reg displ hwy cty
	estimates store hwy_cty
	
	esttab hwy cty hwy_cty using $output_dir/table_reg.tex, replace
end

program city_figure
    scatter cty displ, xtitle("Engine displacement (L)") ///
		ytitle("City fuel economy (mpg)") ///
		mcolor(year)
	graph export $output_dir/figure_city.jpg, replace
end

program hwy_figure
    scatter hwy displ, xtitle("Engine displacement (L)") ///
		ytitle("Highway fuel economy (mpg)") ///
		mcolor(year)
	graph export $output_dir/figure_hwy.jpg, replace
end

* Execute
main

