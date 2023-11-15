install.packages("openxlsx", repos = 'http://cran.us.r-project.org')
library(tidyverse)
library(openxlsx)
set.seed(123)

#### Scalars for gps_primary.xlsx ####

# This is the primary example, based on Table 1 from ad-price-drivers:
# chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://scholar.harvard.edu/files/shapiro/files/ad-price-drivers.pdf

#### Scalars for gs_widetable.xlsx ####

# I'm just manually transcribing from the paper here, of course
# in practice we will compute these ourselves and store in variables.
# In the tables below, I compute random placeholders for the scalars.
data <- t(data.frame(

  c("-1.5556", "(0.2913)", "0.0973", "(0.0292)", "0.0124", "(0.0031)", "103", "809", "", "", "", ""),
  c("-0.0285", "(0.0079)", "-0.4690", "(0.2599)", "0.1221", "(0.0306)", "0.0152", "(0.0034)", "103", "809", "", ""),
  c("-1.6799", "(0.0607)", "0.0082", "(0.0044)", "0.0002", "(0.0004)", "103", "809", "", "", "", ""),
  c("-0.0028", "(0.0024)", "-0.3056", "(0.0933)", "0.0418", "(0.0109)", "0.0057", "(0.0016)", "103", "809", "", ""),
  c("-1.8388", "(0.1027)", "0.0198", "(0.0075)", "0.0102", "(0.0008)", "103", "809", "", "", "", ""),
  c("-0.0020", "(0.0029)", "-0.5230", "(0.1228)", "0.0628", "(0.0125)", "0.0152", "(0.0018)", "103", "809", "", "")

))

# Convert the matrix into a dataframe
vals_df <- as.data.frame(data, stringsAsFactors = FALSE)

# Write the data frame to a .csv and .xlsx file.
write.csv(vals_df, "output/gs_primary_scalars.csv", row.names = FALSE, sep = ";", quote = TRUE)
write.xlsx(vals_df, "output/gs_primary_scalars.xlsx", sheetName = "Placeholders", row.names = FALSE, col.names = FALSE, quote = TRUE)

# Defining placeholder matrix elements
num_columns <- 5
num_rows <- 4
num_rows_ses <- 2

# Generate random values as placeholders.
vals <- as.data.frame(matrix(runif(num_columns * num_rows, min = 0, max = 10), nrow = num_rows))
vals <- round(vals, 3)
vals_parenth <- as.data.frame(matrix(runif(num_columns * num_rows_ses, min = 0, max = 10), nrow = num_rows_ses))
vals_parenth <- round(vals_parenth, 3)
observations_clusters <- as.data.frame(matrix(sample(5000:10000, num_columns * 2, replace = TRUE), nrow = 2))
observations_clusters <- round(observations_clusters)
vals_parenth <- vals_parenth %>% mutate(across(everything(), ~ paste0("(", ., ")")))

# Construct the appended matrix.
combined_data <- rbind(vals, observations_clusters)
combined_data[2,] <- vals_parenth[1,]
combined_data[4,] <- vals_parenth[2,]
combined_data[5:6, ] <- as.character(formatC(as.numeric(as.character(unlist(combined_data[5:6, ]))), big.mark = ",", format = "d", decimal.mark = ""))

# Write the data frame to a .csv and .xlsx file.
write.csv(combined_data, "output/gs_widetable_scalars.csv", row.names = FALSE, sep = ";", quote = TRUE)
write.xlsx(combined_data, "output/gs_widetable_scalars.xlsx", sheetName = "Placeholders", row.names = FALSE, col.names = FALSE, quote = TRUE)

#### Scalars for gs_widetable_extreme.xlsx ####

# I'm intentionally creating a very ugly matrix here, to demonstrate that with this new
# approach where we explicitly form links between sheets; the dimensions of this matrix
# no longer matters. We only need number of filled cells in matrix = number of required scalars in skeleton.
num_columns <- 60
num_rows <- 1

# Generate random values as placeholders.
vals <- sort(runif(num_columns * num_rows, min = 36275, max = 5245121), decreasing = TRUE)
vals <- round(vals)
formatted_vals <- formatC(vals, format = "f", big.mark = ",", digits = 0)
vals_df <- as.data.frame(matrix(formatted_vals, nrow = num_rows))

# Write the data frame to a .csv and .xlsx file.
write.csv(vals_df, "output/gs_widetable_extreme_scalars.csv", row.names = FALSE, sep = ";", quote = TRUE)
write.xlsx(vals_df, "output/gs_widetable_extreme_scalars.xlsx", sheetName = "Placeholders", row.names = FALSE, col.names = FALSE, quote = TRUE)
