import pandas as pd
import numpy as np

### DEFINE
def main():
    tv = pd.read_csv('input/tv.csv')
    chips = pd.read_csv('input/chips.csv')
    df = merge_data(tv, chips)
    df.to_csv('output/data_merged.csv')

def merge_data(tv, chips):
    df = chips.merge(tv, on = 'county_id')
    return(df)

### EXECUTE
main()