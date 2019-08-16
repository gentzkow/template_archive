library(tidyverse)
library(magrittr)
library(rio)

### DEFINE
main <- function() {
  df <- read_csv('output/data_merged.csv')
  plot_data(df)
  df %<>% clean_data()
  df %>% write_csv('output/data_cleaned.csv')
}

plot_data <- function(df) {
  plt <- 
    ggplot(df, aes(x = chips_sold)) + 
    geom_histogram()
  
  ggsave('output/chips_sold.pdf')
}

clean_data <- function(df) {
  df %<>% 
    mutate(chips_sold = ifelse(chips_sold == -999999, NA, chips_sold))
             
  return(df)
}

### EXECUTE
main()
