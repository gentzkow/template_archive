 /**********************************************************
 *
 * LOGS_FOR_TEXTFILL.DO
 * Outputs example stata logs tagged for textfill
 * 
 **********************************************************/ 

version 11
set more off
adopath + ../../external/gslab_misc
preliminaries

program main
    setup_data
    legal
    tags_dont_match
    tag_not_closed
    tags_incorrectly_named
    alternative_prefix
    * I run what would be small_table outside main, so that echoes show up on the logfile
end

program setup_data
    set obs 100
    gen x = uniform()
    gen y = uniform()
end

program legal
    log using ../../log/stata_output_for_textfill/legal.log, replace name(legal_long)
    insert_tag test_long, open
    summ x, det
    summ y, det
    summ
    regress y x
    regress x y
    regress x y, robust
    insert_tag test_long, close
    log close legal_long

    log using ../../log/stata_output_for_textfill/legal.log, append name(legal_short)
    insert_tag test_small, open
    regress y x
    insert_tag test_small, close
    log close legal_short
end    

program tags_dont_match
    log using ../../log/stata_output_for_textfill/tags_dont_match.log, replace name(nomatch)
    insert_tag start, open
    tab x
    tab y
    insert_tag end, close
    log close nomatch
end

program tag_not_closed
    log using ../../log/stata_output_for_textfill/tags_not_closed.log, replace name(noend)
    insert_tag tag, open
    tab x
    tab y
    log close noend
end

program tags_incorrectly_named
    log using ../../log/stata_output_for_textfill/tags_incorrectly_named.log, replace name(badnames)
    insert_tag test_long, open prefix(different)
    tab x
    tab y
    insert_tag test_long, close prefix(different)
    log close badnames
end

program alternative_prefix
    log using ../../log/stata_output_for_textfill/alternative_prefix.log, replace name(prefix_long)
    insert_tag test_long, open prefix(prefix)
    summ x, det
    summ y, det
    summ
    regress y x
    regress x y
    regress x y, robust
    insert_tag test_long, close prefix(prefix)
    log close prefix_long
    
    log using ../../log/stata_output_for_textfill/alternative_prefix.log, append name(prefix_short)
    insert_tag test_small, open prefix(prefix)
    regress y x
    insert_tag test_small, close prefix(prefix)
    log close prefix_short
end

* EXECUTE
main

