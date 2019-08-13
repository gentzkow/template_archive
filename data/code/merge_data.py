###################
### ENVIRONMENT ###
###################
import pandas as pd
import numpy as np

tv = pd.read_csv('input/tv.csv')
chips = pd.read_csv('input/chips.csv')

chips.merge(tv, on = 'county')
