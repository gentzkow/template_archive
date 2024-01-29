import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# =============================================================================

def main():
  mpg_clean = pd.read_csv("../input/mpg.csv")
  regression_table(mpg_clean)
  city_figure(mpg_clean)
  hwy_figure(mpg_clean)

def regression_table(data): 
  reg_cty = sm.OLS.from_formula('displ ~ cty', data).fit()
  print(reg_cty.summary())

  reg_hwy = sm.OLS.from_formula('displ ~ hwy', data).fit()
  print(reg_hwy.summary())

  reg_hwy_cty = sm.OLS.from_formula('displ ~ cty + hwy', data).fit()
  print(reg_hwy_cty.summary())

  latex_table = reg_hwy_cty.summary().as_latex()
  with open("../output/table_reg.tex", "w") as f:
    f.write(latex_table)

def hwy_figure(data):
  plt.scatter(data['displ'], data['hwy'], c=data['year'])
  plt.xlabel("Engine displacement (L)")
  plt.ylabel("Highway fuel economy (mpg)")
  plt.savefig("../output/figure_hwy.jpg")

def city_figure(data):
  plt.scatter(data['displ'], data['cty'], c=data['year'])
  plt.xlabel("Engine displacement (L)")
  plt.ylabel("City fuel economy (mpg)")
  plt.savefig("../output/figure_city.jpg")

# Execute
if __name__ == "__main__":
  main()
