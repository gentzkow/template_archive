/**********************************************************
 *
 * MATRIX_TO_TXT.ADO: Output Matrix as text file
 *
 *  based on Stata add-on mat2txt
 *
 **********************************************************/

capture program drop matrix_to_txt
program define matrix_to_txt

	version 10
	syntax , Matrix(name) SAVing(str) [ REPlace APPend Title(str) Format(str) NOTe(str) USERownames USEColnames]

	if "`format'"=="" local format "%10.0g"
	local formatn: word count `format'
	local saving: subinstr local saving "." ".", count(local ext)
	if !`ext' local saving "`saving'.txt"
	tempname myfile
	file open `myfile' using "`saving'", write text `append' `replace'
	local nrows=rowsof(`matrix')
	local ncols=colsof(`matrix')
	QuotedFullnames `matrix' row
	QuotedFullnames `matrix' col

	* write title
	if "`title'"!="" {
		file write `myfile' `"`title'"' _n
	}

	* write column names
	if "`usecolnames'"!="" {
		if "`userownames'"!="" file write `myfile' _tab
		foreach colname of local colnames {
			file write `myfile' `"`colname'"' _tab
		}
		file write `myfile' _n
	}

	* write body of table
	forvalues r=1/`nrows' {
		if "`userownames'"!="" {
			local rowname: word `r' of `rownames'
			file write `myfile' `"`rowname'"' _tab
		}
		forvalues c=1/`ncols' {
			if `c'<=`formatn' local fmt: word `c' of `format'
			file write `myfile' `fmt' (`matrix'[`r',`c'])
			if `c'<`ncols' {
				file write `myfile' _tab
			}
		}
		file write `myfile' _n
	}
	if "`note'"!="" {
	file write `myfile' `"`note'"' _n
	}
	file close `myfile'

end

capture program drop QuotedFullnames
program define QuotedFullnames
	args matrix type
	tempname extract
	local one 1
	local i one
	local j one
	if "`type'"=="row" local i k
	if "`type'"=="col" local j k
	local K = `type'sof(`matrix')
	forv k = 1/`K' {
		mat `extract' = `matrix'[``i''..``i'',``j''..``j'']
		local name: `type'names `extract'
		local eq: `type'eq `extract'
		if `"`eq'"'=="_" local eq
		else local eq `"`eq':"'
		local names `"`names'`"`eq'`name'"' "'
	}
	c_local `type'names `"`names'"'
end
