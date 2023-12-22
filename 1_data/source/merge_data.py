import pandas as pd
import numpy as np
import os

# DEFINE PATHS
input_raw=os.environ["INPUT_RAW"]
output=os.environ["OUTPUT"]

### DEFINE
def main():
    tv = pd.read_csv(f"{input_raw}/tv.csv")
    chips = pd.read_csv(f"{input_raw}/chips.csv")
    df = merge_data(tv, chips)
    df.to_csv(f"{output}/data_merged.csv", index = False)

def merge_data(tv, chips):
    df = chips.merge(tv, on = 'county_id')
    return(df)

### EXECUTE
main()
