library(yaml)

main <- function() {
  x <- read.csv("input/data.csv")
  x["x"] <- x["x"] * 2
  write.csv(x, "output/data_table.csv", row.names = FALSE)
}

# EXECUTE
main()