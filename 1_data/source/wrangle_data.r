# =============================================================================
# Short description of script's purpose
# =============================================================================

library(tidyverse)

# Paths
input_dir <- "../../0_raw"
output_dir <- "../output"

# =============================================================================

main <- function() {
  mpg <- read.csv(file.path(input_dir, "mpg.csv"))
  mpg_clean <- clean_data(mpg)
  save(mpg_clean, file = file.path(output_dir, "mpg.Rdata"))
}

clean_data <- function(mpg) {
  # Some data wrangling steps here
  mpg_clean <- mpg 
  return(mpg_clean)
}

# Execute
main()
