program standardize_env
	version 15

	*  Remove all non-base paths from the ado path
	adopath - PERSONAL
	adopath - PLUS
	adopath - OLDPLACE
	adopath - SITE

	adopath + "input/lib/stata/ado"
	adopath + "input/lib/ado"
end

exit
