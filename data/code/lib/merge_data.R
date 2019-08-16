library(tidyverse)
library(magrittr)

follow_link <- R.utils::Sys.readlink2

### DEFINE
main <- function() {
  tv <- follow_link('input/tv.csv') %>% read_csv
  chips <- follow_link('input/chips.csv') %>% read_csv
  df <- merge_data(tv, chips)
  df %>% write_csv('output/data_merged.csv')
}

merge_data <- function(tv, chips) {
  df <-
    left_join(tv, chips, by = c('county_id'))

  return(df)
}

### EXECUTE
main()