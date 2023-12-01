install.packages("openxlsx", repos = 'http://cran.us.r-project.org')
library(tidyverse)
library(openxlsx)
set.seed(123)

#### Scalars for gps_primary.xlsx ####

# This is the primary example, based on Table 1 from the paper:
# Pricing Power in Advertising Markets: Theory and Evidence (see link below, table on pg. 90):
# https://scholar.harvard.edu/files/shapiro/files/ad-price-drivers.pdf

#### Scalars for gs_widetable.xlsx ####

# Here, we are manually transcribing values from the paper here. Of course
# in practice, users should compute these scalars themselves and store
# the outputs in variables (in other ~/analysis/code scripts).
data <- t(data.frame(

  c("-1.5556", "(0.2913)", "0.0973", "(0.0292)", "0.0124", "(0.0031)", "103", "809", "", "", "", ""),
  c("-0.0285", "(0.0079)", "-0.4690", "(0.2599)", "0.1221", "(0.0306)", "0.0152", "(0.0034)", "103", "809", "", ""),
  c("-1.6799", "(0.0607)", "0.0082", "(0.0044)", "0.0002", "(0.0004)", "103", "809", "", "", "", ""),
  c("-0.0028", "(0.0024)", "-0.3056", "(0.0933)", "0.0418", "(0.0109)", "0.0057", "(0.0016)", "103", "809", "", ""),
  c("-1.8388", "(0.1027)", "0.0198", "(0.0075)", "0.0102", "(0.0008)", "103", "809", "", "", "", ""),
  c("-0.0020", "(0.0029)", "-0.5230", "(0.1228)", "0.0628", "(0.0125)", "0.0152", "(0.0018)", "103", "809", "", "")

))

# Convert the matrix into a dataframe.
vals_df <- as.data.frame(data, stringsAsFactors = FALSE)

# We write the data frame to a .csv and .xlsx file (this allows for git tracking).
write.csv(vals_df, "output/tables/gs_primary_scalars.csv", row.names = FALSE, sep = ";", quote = TRUE)
write.xlsx(vals_df, "output/tables/gs_primary_scalars.xlsx", sheetName = "Placeholders", row.names = FALSE, col.names = FALSE, quote = TRUE)
