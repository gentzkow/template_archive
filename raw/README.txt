================================================================================
OVERVIEW
================================================================================
Raw data and source files

================================================================================
SOURCE
================================================================================
N/A

================================================================================
WHEN/WHERE OBTAINED & ORIGINAL FORM OF FILES
================================================================================
`data.csv` self-generated on 2019-05-08

================================================================================
DESCRIPTION
================================================================================
Generated data for example scripts in template repository

================================================================================
NOTES
================================================================================
`data.csv` generated using the following R code:

```
x <- 1:300000
write.table(x, "data.csv", row.names = FALSE, col.names = TRUE, quote = FALSE)
```

# ~~~~~~~~~~~~
# Environment
# ~~~~~~~~~~~~
library(pacman)
p_load(tidyverse, magrittr)
set.seed(1)

# ~~~~~~~~~~
# Randomize
# ~~~~~~~~~~

tv <- 
  data.frame(
    county = 1:10000, 
    size = runif(10000),
    year_tv_introduced = 1950 + sample.int(10, size = 10000, replace = T)
  )
  
chips <-
  data.frame(
    expand.grid(county = 1:10000, year = 1940:1970)
  )

chips %<>%
  left_join(tv, by = c('county'))

chips %<>% 
  mutate(post_tv = (year > year_tv_introduced)) %>%
  mutate(chips_sold = 10000*size + rnorm(10000, mean = 0, sd = 100)) %>%
  mutate(chips_sold = chips_sold + 1000*post_tv + (year - 1940) * 100)