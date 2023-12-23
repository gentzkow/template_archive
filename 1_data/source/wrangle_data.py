"""Short description of script's purpose

"""

import pandas as pd
import numpy as np

# Paths
input_dir = '../../0_raw'
output_dir = '../output'

# =============================================================================

def main():
  mpg = pd.read_csv(f"{input_dir}/mpg.csv")
  mpg_clean = clean_mpg_data(mpg)
  mpg_clean.to_csv(f"{output_dir}/mpg.csv", index = False)

def clean_mpg_data(mpg):
  # Data wrangling steps here
  mpg_clean = mpg 
  return(mpg_clean)

# Execute
if __name__ == "__main__":
	main()