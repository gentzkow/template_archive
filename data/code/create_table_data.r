library(yaml)

main <- function() {
  x <- 1:300000
  write.table(x, "output/data_table.csv", row.names = FALSE, col.names = TRUE, quote = FALSE)
}

# EXECUTE
main()