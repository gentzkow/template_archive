library(yaml)

main <- function() {
  x <- read.csv("input/data.csv")
  write.csv(x, "output/data_table.csv", row.names = FALSE)
}

# EXECUTE
main()