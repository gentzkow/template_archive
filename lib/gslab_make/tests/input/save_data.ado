program save_data
    version 11
    syntax anything(name=filename) [if], key(varlist) [outsheet log_replace log(str) missok* nopreserve]
    if "`preserve'"!="nopreserve" {
        preserve
    }
    
    if "`if'"!="" {
        keep `if'
    }
    isid `key', sort `missok'
    order `key', first
    compress
    
    local default = "data_file_manifest.log"
    * Define default log value
    if "`log'"=="" {
        define_default_log_file log, filename(`filename') default(`default')
    }
    
    if "`log_replace'"!="" {
        print_info_to_log using `log', filename(`filename') key(`key') overwrite
    }
    else {
        print_info_to_log using `log', filename(`filename') key(`key')
    }
    
    if "`outsheet'"!="" {
        outsheet using `filename', `options'
    }
    else {
        save `filename', `options'
    }
    
    if "`preserve'"!="nopreserve" {
        restore
    }
end

program define_default_log_file
    syntax anything(name=local), filename(string) default(string)
    if regexm("`filename'", "(\/output\/)(.+\/)") == 1 {
        local newdir = regexs(1) + regexs(2) + "`default'"
        c_local `local' "../`newdir'"
    } 
    else if regexm("`filename'", "(\/output\/)") == 1 {
        local newdir = regexs(1) + "`default'"
        c_local `local' "../`newdir'"
    }
    else {
        c_local `local' "none"
    }
end

program print_info_to_log
    syntax using/, filename(str) key(varlist) [nolog overwrite]
    
    if "`using'"~="none" {
        if "`overwrite'"!=""{
            qui log using `using', text replace name(save_data_log)
        }
        else{
            qui log using `using', text append name(save_data_log)
        }
    }
    di "=================================================================================================="
    if regexm("`filename'", "\.") == 0 {    
        di "File: `filename'.dta"
    }
    else {
        di "File: `filename'"
    }    
    di "Key: `key'"
    di "=================================================================================================="
    datasignature
    sum
    di ""
    di ""
    di ""
    di ""
    cap log close save_data_log 
end
