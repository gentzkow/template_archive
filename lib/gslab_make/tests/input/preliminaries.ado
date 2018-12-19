 /**********************************************************
 *
 *  PRELIMINARIES.ADO: SET PRELIMINARIES FOR DO FILES
 * 
 * Inputs: 1) Standard inputs to stata file:
 *                a) maxvar (default 5000)
 *                b) matsize (default 5000)
 *                c) sortseed
 *                d) seed 
 *                e) linesize (default 255)
 *                f) loadglob (space-delimited list of global variable files)
 * 
 * Output: 1) Message about any errors printed to the log
 * 
 **********************************************************/ 
version 12

program define preliminaries
 
    quietly{
        
        syntax , [matsize(string) maxvar(string) sortseed(string) linesize(string) loadglob(string) seed(string)]  
    
        if "`sortseed'"==""{
            local sortseed 47
        }    
        if "`matsize'"==""{
            local matsize 5000
        }    
        if "`linesize'"==""{
            local linesize 255
        }
        if "`maxvar'"==""{
            local maxvar 5000
        }
        if "`seed'"==""{
            local seed 147
        }
        
        clear all
        
        set matsize `matsize'
        set linesize `linesize'
        set maxvar `maxvar'
        set sortseed `sortseed'
        set seed `seed'
        
        if "`loadglob'"!=""{
            foreach globfile of local loadglob {
                loadglob using `globfile'
            }
        }
    }
end
