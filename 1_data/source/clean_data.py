import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paths
output='../output'

df = pd.read_csv(f'{output}/data_merged.csv')
df.loc[df['chips_sold'] == -999999, 'chips_sold'] = np.nan
df.to_csv(f'{output}/data_cleaned.csv', index = False)
