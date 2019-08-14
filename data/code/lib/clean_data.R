import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### DEFINE
def main():
    df = pd.read_csv('output/data_merged.csv')
    plot_data(df)
    df = clean_data(df)
    df.to_csv('output/data_cleaned.csv')

def plot_data(df):
    plt.hist(df['chips_sold'])
    plt.savefig('output/chips_sold.pdf')

def clean_data(df):
    df[df['chips_sold'] == -999999] = np.NaN
    return(df)
    
### EXECUTE
main()
