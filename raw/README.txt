--------------------------------------------------------------------------------
OVERVIEW
--------------------------------------------------------------------------------
Generated data for TV & potato chips example scripts in template repository

--------------------------------------------------------------------------------
SOURCE
--------------------------------------------------------------------------------
N/A

--------------------------------------------------------------------------------
WHEN/WHERE OBTAINED & ORIGINAL FORM OF FILES
--------------------------------------------------------------------------------
`tv.csv` 
  - Self-generated on 2019-09-13

`chips.csv`
  - Self-generated on 2019-09-13

--------------------------------------------------------------------------------
DESCRIPTION
--------------------------------------------------------------------------------
`tv.csv`
  - Year that TV was first introduced for each county in the US

`chips.csv`
  - Total sales of potato chips by county by year from 1940 to 1970

--------------------------------------------------------------------------------
NOTES
--------------------------------------------------------------------------------
`tv.csv` and `chips.csv` were generated using the following R code:

```
# Environment
library(tidyverse)
library(magrittr)
set.seed(1)

n_counties <- 1e4
error_rate <- 0.01
error_prob <- c(1 - error_rate, error_rate)

# Generate TV data
tv <- 
  data.frame(
    county_id = 1:n_counties, 
    county_size = runif(n_counties),
    year_tv_introduced = 1950 + sample.int(10, size = n_counties, replace = T)
  )

# Generate chips data
chips <-
  expand.grid(
    county_id = 1:n_counties, 
    year = 1940:1970 
  ) %>% 
  as.data.frame 

chips %<>%
  left_join(tv, by = c('county_id'))

chips %<>% 
  mutate(post_tv = (year > year_tv_introduced)) %>%
  mutate(chips_sold = county_size + 0.1*post_tv + (year - 1940) * 0.01) %>%
  mutate(chips_sold = county_size + runif()) %>%
  mutate(chips_sold = chips_sold * 1e6)

# Introduce error to chips data
chips %<>%
  mutate(error = sample(c(0, 1), size = nrow(.), prob = error_prob, replace = T)) %>%
  mutate(chips_sold = ifelse(error == 1, -999999, chips_sold))

# Export data
tv %>%
  select(county_id, year_tv_introduced) %>%
  write_csv('tv.csv')

chips %>%
  select(county_id, year, chips_sold) %>%
  write_csv('chips.csv')
```