clear all
set more off, perm

version 15

adopath - PERSONAL
adopath - OLDPLACE
adopath - SITE

sysdir set PLUS "../lib/ado"

program main
	* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	* Add required packages from SSC to this list
	* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	local ssc_packages ""
	
    if !missing("`ssc_packages'") {
        foreach pkg in `ssc_packages' {
			capture which `pkg'
			if _rc == 111 {			
				dis "Installing `pkg'"
                quietly ssc install `pkg', replace
			}
        }
    }

    * Install packages using net
    capture which yaml
	if _rc == 111 {
        quietly net from "https://raw.githubusercontent.com/gslab-econ/stata-misc/master/"
        quietly cap ado uninstall yaml
        quietly net install yaml
	}
	
    capture which matrix_to_txt
	if _rc == 111 {
        quietly net from "https://raw.githubusercontent.com/gslab-econ/gslab_stata/master/gslab_misc/ado"
        quietly cap net uninstall matrix_to_txt
        quietly net install matrix_to_txt
	}

	capture which preliminaries
	if _rc == 111 {
        quietly net from "https://raw.githubusercontent.com/gslab-econ/gslab_stata/master/gslab_misc/ado"
        quietly cap net uninstall preliminaries
        quietly net install preliminaries
	}	
	
	capture which grc1leg
	if _rc == 111 {
		quietly net from "http://www.stata.com/users/vwiggins"
		quietly cap net uninstall grc1leg
		quietly net install grc1leg
	}
end

main
