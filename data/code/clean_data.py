import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import data
df = pd.read_csv('output/data_merged.csv')

# Descriptive statistics
df['chips_sold'].describe()
df['chips_sold'].hist()

plt.savefig('output/chips_sold.pdf')

# Clean data
df[df['chips_sold'] == -999999] = np.NaN

# Export data
df.to_csv('output/data_cleaned.csv')