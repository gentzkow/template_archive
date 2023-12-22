# from gentzkow/template: https://github.com/gentzkow/template/blob/master/analysis/code/analyze_data.py
import pandas as pd
import numpy as np
from linearmodels import PanelOLS
import os

# DEFINE PATHS
input_raw=os.environ["INPUT_DATA"]
output=os.environ["OUTPUT"]

### DEFINE
def main():
    df = import_data()
    fit = run_regression(df)
    formatted = format_model(fit)
    
    with open(f'{output}/regression.csv', 'w') as f:
        f.write('<tab:regression>' + '\n')
        formatted.to_csv(f, sep = '\t', index = False, header = False)
    
def import_data():
    df = pd.read_csv(f'{input_raw}/data_cleaned.csv')
    df['post_tv'] = df['year'] > df['year_tv_introduced']
    
    return(df)

def run_regression(df):
    # drop missing values of chips_sold or post_tv
    df = df.dropna(subset = ['chips_sold', 'post_tv'])
    df = df.set_index(['county_id', 'year'])
    model = PanelOLS.from_formula('chips_sold ~ 1 + post_tv + EntityEffects + TimeEffects', data = df)
    fit = model.fit()
    
    return(fit)
    
def format_model(fit):
    formatted = pd.DataFrame({'coef'     : fit.params, 
                              'std_error': fit.std_errors, 
                              'p_value'  : fit.pvalues})
    formatted = formatted.loc[['post_tv']]
    
    return(formatted)
    
### EXECUTE
main()