library(tidyverse)
library(magrittr)
library(plm)
library(janitor)

follow_link <- R.utils::Sys.readlink2 # tidyverse packages have difficulty reading Windows symlinks

options(scipen = 999)

### DEFINE
main <- function() {
  df <- import_data()
  fit <- run_regression(df)
  formatted <- format_model(fit)
  write_lines('<tab:regression>', 'output/regression.csv')
  formatted %>% write_delim('output/regression.csv', delim = '\t', col_names = F, append = T)
}

import_data <- function() {
  df <- follow_link('input/data_cleaned.csv') %>% read_csv
  df %<>% mutate(post_tv = (year > year_tv_introduced))
    
  return(df)
}

run_regression <- function(df) {
  df %<>% pdata.frame(index = c('county_id', 'year'))
  
  fit <- plm(chips_sold ~ post_tv, data = df, model = 'within', effect = 'twoways')
  
  return(fit)
}

format_model <- function(fit) {
  fit %<>% summary
  
  formatted <- 
    fit$coefficients %>%
    as.data.frame 
  
  formatted %<>%
    clean_names %>%
    select(estimate, std_error, pr_t)
  
  return(formatted)
}

### EXECUTE
main()