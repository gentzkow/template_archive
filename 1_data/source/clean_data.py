import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# DEFINE PATHS
output=os.environ["OUTPUT"]

### DEFINE
def main():
    df = pd.read_csv(f'{output}/data_merged.csv')
    plot_data(df)
    df = clean_data(df)
    df.to_csv(f'{output}/data_cleaned.csv', index = False)

def plot_data(df):
    plt.hist(df['chips_sold'])
    plt.savefig(f'{output}/chips_sold.pdf')

def clean_data(df):
    # df['chips_sold'][df['chips_sold'] == -999999] = np.NaN
    df.loc[df['chips_sold'] == -999999, 'chips_sold'] = np.nan
    return(df)
    
### EXECUTE
main()
