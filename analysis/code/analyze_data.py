import pandas as pd
import numpy as np
from linearmodels import PanelOLS

### DEFINE
def main():
    df = import_data()
    fit = run_regression(df)
    formatted = format_model(fit)
    
    with open('output/regression.csv', 'w') as f:
        f.write('<tab:regression>' + '\n')
        formatted.to_csv(f, sep = '\t', index = False, header = False)

    fit_cls = run_regression_cls(df)
    formatted_cls = format_model(fit_cls)
    
    with open('output/regression_cls.csv', 'w') as f:
        f.write('<tab:regression_cls>' + '\n')
        formatted_cls.to_csv(f, sep = '\t', index = False, header = False)

    # Run the regression on subset of years greater or equal to 1960
    df_ge1960 = df[df['year'] >= 1960].copy()
    fit_ge1960 = run_regression(df_ge1960)
    formatted_ge1960 = format_model(fit_ge1960)
    
    with open('output/regression_ge1960.csv', 'w') as f:
        f.write('<tab:regression_ge1960>' + '\n')
        formatted_ge1960.to_csv(f, sep = '\t', index = False, header = False)


    fit_ge1960_cls = run_regression_cls(df_ge1960)
    formatted_ge1960_cls= format_model(fit_ge1960_cls)
    
    with open('output/regression_ge1960_cls.csv', 'w') as f:
        f.write('<tab:regression_ge1960_cls>' + '\n')
        formatted_ge1960_cls.to_csv(f, sep = '\t', index = False, header = False)
    
def import_data():
    df = pd.read_csv('input/data_cleaned.csv')
    df['post_tv'] = df['year'] > df['year_tv_introduced']
    
    return(df)

def run_regression(df):
    df = df.set_index(['county_id', 'year'])
    model = PanelOLS.from_formula('chips_sold ~ 1 + post_tv + EntityEffects + TimeEffects', data = df)
    fit = model.fit()
    
    return(fit)
    
def run_regression_cls(df):
    df = df.set_index(['county_id', 'year'])
    model = PanelOLS.from_formula('chips_sold ~ 1 + post_tv + EntityEffects + TimeEffects', data = df)
    fit = model.fit(cov_type='clustered', cluster_entity=True)
    return(fit)
    
def format_model(fit):
    formatted = pd.DataFrame({'coef'     : fit.params, 
                              'std_error': fit.std_errors, 
                              'p_value'  : fit.pvalues})
    formatted = formatted.loc[['post_tv']]
    
    return(formatted)
    
### EXECUTE
main()