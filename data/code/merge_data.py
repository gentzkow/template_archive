import pandas as pd
import numpy as np

# Import data
tv = pd.read_csv('input/tv.csv')
chips = pd.read_csv('input/chips.csv')

# Merge data
df = chips.merge(tv, on = 'county_id')

# Export data
df.to_csv('output/data_merged.csv')