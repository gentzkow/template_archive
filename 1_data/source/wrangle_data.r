# =============================================================================
# Short description of script's purpose
# =============================================================================

library(tidyverse)

# =============================================================================

main <- function() {
  mpg <- read.csv("../input/mpg.csv")
  mpg_clean <- clean_data(mpg)
  save(mpg_clean, file = "../output/mpg.Rdata")
}

clean_data <- function(mpg) {
  # Some data wrangling steps here
  mpg_clean <- mpg 
  return(mpg_clean)
}

# Execute
main()
