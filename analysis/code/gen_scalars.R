install.packages("openxlsx", repos = 'http://cran.us.r-project.org')
library(tidyverse)
library(openxlsx)
set.seed(123)

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

# Write the data frame to a .txt and .xlsx file.
write.csv(combined_data, "output/gps_scalars.csv", row.names = FALSE, sep = ";", quote = TRUE)
write.xlsx(combined_data, "output/gps_scalars.xlsx", sheetName = "Placeholders", row.names = FALSE, col.names = FALSE, quote = TRUE)