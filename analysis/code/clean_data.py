
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels import PanelOLS

tv = pd.read_csv('input/tv.csv')
chips = pd.read_csv('input/chips.csv')

df = chips.merge(tv, on = 'county_id')

df['chips_sold'].describe()

plot = df['chips_sold'].hist()

df['post_tv'] = df['year'] > df['year_tv_introduced']

Y = df['chips_sold']
X = df['post_tv']
model = LinearRegression()
model = model.fit(Y, X)