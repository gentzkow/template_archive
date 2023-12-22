"""Merge tv and chips datasets

"""

import pandas as pd
import numpy as np

# Paths
repo_root = '../..'
input = f'{repo_root}/0_raw'
output = '../output'

def main():
	tv = pd.read_csv(f"{input}/tv.csv")
	chips = pd.read_csv(f"{input}/chips.csv")
	
	df = merge_data(chips, tv, 'county_id')
	
	df.to_csv(f"{output}/data_merged.csv", index = False)

def merge_data(left_data, right_data, merge_var):
	df = left_data.merge(right_data, on = merge_var)
	return df

# Execute
if __name__ == "__main__":
	main()
