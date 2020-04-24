# -*- coding: utf-8 -*-
"""
Macro Analysis:
Objective: Calculate GDP nowcast, calculate likeliest forward path, project returns based on economic data
inputs: FRED data, historical prices
outputs: nowcast, forecast, return correlations
todo: functionalize fit to include normalization, rolling sum, gold model, bitcoin model, look at SAAR points, try z-score for heatmap
       

"""

import pandas as pd
import numpy as np
import seaborn as sns
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import statsmodels.api as sm
import plotly.express as px
from plotly.offline import plot

#initializations
sns.set()

#pull giant historical list of data from Fred
start = dt.datetime(1980, 1, 1)
end = dt.date.today()
macro_data = pdr.get_data_fred(['USAGDPDEFQISMEI','NA000334Q','ND000334Q','GDPC1','CPIAUCSL','PCEC96','PCECC96','RSAFS','RRSFS','DSPIC96','RSAOMV','PSAVERT','PAYEMS','PRSCQ','CES0500000017','ICSA','CCSA','UMCSENT',
                                'MICH','CSCICP03USM665S','M1','M2','INDPRO','DGORDER','NEWORDER','BUSINV','TLNRESCONS','TLRESCONS','NETEXP','IMPGSC1','EXPGSC1','BOPGSTB',
                                'DPCERD3Q086SBEA','CPILFESL','DCOILWTICO'], start, end)

############### Begin Analysis ###############
#convert nominal quarterly data to real using implicit deflator, calculate a trailing four quarter average
macro_data.loc[:,'realGDP'] = .1*(macro_data.loc[:,'NA000334Q']/macro_data.loc[:,'USAGDPDEFQISMEI'])
gdp_data = macro_data.loc[:,'realGDP'].dropna()
gdp_data_trailing = gdp_data.rolling(window=4).sum()

#initialize series long name dictionary and dictionary of how many data points are required to annualize
#divisor = {} 
series_name= {}
points_required = {}

#list of tickers to include for outright model
regression_list = ['PCEC96', 'PCECC96','RSAFS','RRSFS','RSAOMV','PRSCQ','CES0500000017','INDPRO','DGORDER','NEWORDER','BUSINV','TLNRESCONS','TLRESCONS','NETEXP','IMPGSC1','EXPGSC1','BOPGSTB']
#for ticker in regression_list:
#    divisor[ticker] = 1

for ticker in regression_list:
    points_required[ticker] = 4
    
for ticker in regression_list:
    series_name[ticker] = ticker

series_name['PCEC96'] = 'Real Personal Consumption Expenditures (Monthly)'
series_name['PCECC96'] = 'Real Personal Consumption Expenditures (Quarterly)'
series_name['RSAFS'] = 'Advance Retail Sales (Monthly)'
series_name['RRSFS'] = 'Advance Retail Sales: Real (Monthly)'
series_name['DSPIC96'] = 'Real Disposable Personal Income (Monthly)'
series_name['RSAOMV'] = 'Motor Vehicle Sales (Monthly)'
series_name['PRSCQ'] = 'Hours Worked, Nonfarm (Quarterly)'
series_name['CES0500000017'] = 'Aggregate Weekly Payrolls (Monthly)'
series_name['INDPRO'] = 'Industrial Production (Monthly)'
series_name['DGORDER'] = 'Durable Goods Orders (Monthly) [needs deflator]'
series_name['NEWORDER'] = 'Nondefense Capital Goods Orders (Monthly) [needs deflator]'
series_name['BUSINV'] = 'Business Inventories (Monthly) [needs deflator]'
series_name['TLNRESCONS'] = 'Nonresidential Construction SAAR (Monthly) [needs deflator]'
series_name['TLRESCONS'] = 'Residential Construction SAAR (Monthly) [needs deflator]'
series_name['NETEXP'] = 'Net Exports [SAAR, Quarterly]'
series_name['IMPGSC1'] = 'Real Imports [SAAR, Quarterly]'
series_name['EXPGSC1'] = 'Real Exports [SAAR, Quarterly]'
series_name['BOPGSTB'] = 'Trade Balance [SAAR, Quarterly]'

points_required['PCEC96'] = 12
points_required['PCECC96'] = 4
points_required['RSAFS'] = 12
points_required['RRSFS'] = 12
points_required['RSAOMV'] = 12
points_required['PRSCQ'] = 4
points_required['INDPRO'] = 12
points_required['DGORDER'] = 12
points_required['NEWORDER'] = 12
points_required['BUSINV'] = 12
points_required['TLRESCONS'] = 1
points_required['NETEXP'] = 1
points_required['IMPGSC1'] = 1
points_required['EXPGSC1'] = 1
points_required['BOPGSTB'] = 12

#initialize dictionaries of regression models and data used
gdp_model = {}
prediction_data = {}
comp_data = {}

gdp_data = macro_data.loc[:,'realGDP'].dropna()
gdp_data_t12m = gdp_data.rolling(window=4).sum().dropna()

#model gdp for each factor
for ticker in regression_list:
    comp_data[ticker] = macro_data.loc[:,ticker].dropna().rolling(window=points_required[ticker]).sum()
    prediction_data[ticker] = pd.merge_asof(left=gdp_data_t12m, right=comp_data[ticker], left_index=True, right_index=True, direction='backward')
    prediction_data[ticker] = prediction_data[ticker].dropna()

    gdp_regression = sm.OLS(prediction_data[ticker].loc[:,'realGDP'], prediction_data[ticker].loc[:,ticker])
    gdp_model[ticker] = gdp_regression.fit()
    print(series_name[ticker] + ' r-squared value: ' + '{:.3%}'.format(gdp_model[ticker].rsquared))
''
def macro_table():
    return macro_data

def gdp_history():
    return gdp_data,gdp_data_t12m

def scatter_data_gdp():
    return regression_list, comp_data, prediction_data, series_name, points_required, gdp_model

def macro_heatmap():
    return (pd.merge_asof(left=gdp_data_t12m, right=macro_data.loc[:,regression_list], left_index=True, right_index=True, direction='backward').pct_change()).transpose()


# fig = px.scatter(x=prediction_data.loc[:,ticker].values, y=prediction_data.loc[:,'GDPC1'].values)
# plot(fig)
# fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
#fig.show()


