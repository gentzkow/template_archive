# =============================================================================
# Short description of script's purpose
# =============================================================================

library(tidyverse)
library(stargazer)
library(ggplot2)

# Paths
input_dir <- "../../1_data/output"
output_dir <- "../output"

# =============================================================================

main <- function() {
  load(file.path(input_dir, "mpg.Rdata"))
  regression_table(mpg_clean)
  city_figure(mpg_clean)
  hwy_figure(mpg_clean)
}

regression_table <- function(data) {
  reg_cty <- lm(displ ~ cty, data = data)
  summary(reg_cty)

  reg_hwy <- lm(displ ~ hwy, data = data)
  summary(reg_hwy)

  reg_hwy_cty <- lm(displ ~ hwy + cty, data = data)
  summary(reg_hwy_cty)

  stargazer(reg_cty, reg_hwy, reg_hwy_cty, title = "Results", align = TRUE,
            dep.var.labels = c("Engine displacement (L)"),
            covariate.labels = c("City fuel economy (mpg)",
                                 "Highway fuel economy (mpg)"),
            out = file.path(output_dir, "table_reg.tex"))
}

city_figure <- function(data) {
  p <- ggplot(data, aes(x = displ, y = cty, color = year)) +
    geom_point() +
    xlab("Engine displacement (L)") +
    ylab("City fuel economy (mpg)")
  ggsave(file.path(output_dir, "figure_city.jpg"), plot = p)
}

hwy_figure <- function(data) {
  p <- ggplot(data, aes(x = displ, y = hwy, color = year)) +
    geom_point() +
    xlab("Engine displacement (L)") +
    ylab("Highway fuel economy (mpg)")
  ggsave(file.path(output_dir, "figure_hwy.jpg"), plot = p)
}

# Execute
main()
