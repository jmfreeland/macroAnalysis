# -*- coding: utf-8 -*-
"""
Portfolio Construction:
Objective: Calculate approximate forward return and scale accepted risk up or down accordingly.
inputs: FRED data on spreads and total returns, MOVE Index, yield curve, VIX and returns
outputs: Location of current spreads in historical range, forward return 
            projections, spread change projections
    
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

#pull Investment Grade spreads, total return data from FRED 
start = dt.datetime(1980, 1, 1)
end = dt.date.today()
macro_data = pdr.get_data_fred(['USAGDPDEFQISMEI','NA000334Q','ND000334Q','GDPC1','CPIAUCSL','PCEC96','PCECC96','RSAFS','RRSFS','DSPIC96','RSAOMV','PSAVERT','PAYEMS','PRSCQ','B4701C0A222NBEA','CES0500000017','ICSA','CCSA','UMCSENT',
                                'MICH','CSCICP03USM665S','M1','M2','INDPRO','DGORDER','NEWORDER','BUSINV','TLNRESCONS','TLRESCONS','DCOILWTICO','NETEXP','IMPGSC1','EXPGSC1','BOPGSTB',
                                'DPCERD3Q086SBEA','CPILFESL','DCOILWTICO'], start, end)
macro_data.loc[:,'realGDP'] = .1*(macro_data.loc[:,'NA000334Q']/macro_data.loc[:,'USAGDPDEFQISMEI'])
gdp_data = macro_data.loc[:,'realGDP'].dropna()
gdp_data_trailing = gdp_data.rolling(window=4).sum()


divisor = {}

regression_list = ['PCEC96']
for ticker in regression_list:
    divisor[ticker] = 1;
    

test_targets = []

convert_to_real = []
series_name={}

series_name['PCEC96'] = 'Real Personal Consumption Expenditures'

gdp_model = {}
prediction_data = {}
ticker='PCEC96'
gdp_data = macro_data.loc[:,'realGDP'].dropna()
gdp_data_t12m = gdp_data.rolling(window=4).sum().dropna()

#for ticker in regression_list:
comp_data = macro_data.loc[:,ticker]
prediction_data[ticker] = pd.merge_asof(left=gdp_data_t12m, right=comp_data, left_index=True, right_index=True, direction='backward')
prediction_data[ticker] = prediction_data[ticker].dropna()

gdp_regression = sm.OLS(prediction_data[ticker].loc[:,'realGDP'], prediction_data[ticker].loc[:,ticker])
gdp_model[ticker] = gdp_regression.fit()
gdp_model[ticker].summary()



def macro_table():
    return macro_data

def gdp_history():
    return gdp_data,gdp_data_t12m

# fig = px.scatter(x=prediction_data.loc[:,ticker].values, y=prediction_data.loc[:,'GDPC1'].values)
# plot(fig)
# fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
#fig.show()


#predict outright GDP


# fig = plt.figure(figsize=[8,8])
# plt.title("ICE BofA IG Spread Histogram, 1996-")

# sns.distplot(IG_ICE_data.loc[:,'BAMLC0A0CM'], bins=50, label='IG', hist_kws={"alpha": .7})
# sns.distplot(IG_ICE_data.loc[:,'BAMLC0A4CBBB'], bins=50, label='BBB', hist_kws={"alpha": .1})
# sns.distplot(IG_ICE_data.loc[:,'BAMLC8A0C15PY'], bins=50, label='15Y+', color='purple', hist_kws={"alpha": .1})

# plt.xlabel('IG (blue), BBB (orange), 15yt+ (purple)')
# IG_ICE_quantile = IG_ICE_data.loc[:,'BAMLC0A0CM'].rank(pct=True)[-1]
# BBB_ICE_quantile = IG_ICE_data.loc[:,'BAMLC0A4CBBB'].rank(pct=True)[-1]
# Long_ICE_quantile = IG_ICE_data.loc[:,'BAMLC8A0C15PY'].rank(pct=True)[-1]

# print("ICE/BofA IG spreads of " + str(100*IG_ICE_data.loc[:,'BAMLC0A0CM'][-1]) + "bp are higher than " + '{:.1%}'.format(IG_ICE_quantile) + " of history (1919-current)")
# print("ICE/BofA BBB spreads of " + str(100*IG_ICE_data.loc[:,'BAMLC0A4CBBB'][-1]) + "bp are higher than " + '{:.1%}'.format(BBB_ICE_quantile) + " of history (1919-current)")
# print("ICE/BofA 15yr+ spreads of " + str(100*IG_ICE_data.loc[:,'BAMLC8A0C15PY'][-1]) + "bp are higher than " + '{:.1%}'.format(Long_ICE_quantile) + " of history (1919-current)")

# #print("1yr. forward yield change from this level is typically: ")

# start = dt.datetime(1919, 1, 1)
# end = dt.date.today() 
# IG_moodys_data = pdr.get_data_fred(['BAA','AAA'], start, end)
# IG_moodys_daily = pdr.get_data_fred(['DBAA','DAAA'], end + dt.timedelta(days=-7), end)
# IG_moodys_data.loc[IG_moodys_daily.index[-1],'BAA'] = IG_moodys_daily.loc[:,'DBAA'][-1]
# IG_moodys_data.loc[IG_moodys_daily.index[-1],'AAA'] = IG_moodys_daily.loc[:,'DAAA'][-1]

# fig = plt.figure(figsize=[8,8])
# plt.title("Moody's Baa/Aaa Yield Histogram, 1919-")
# sns.distplot(IG_moodys_data.loc[:,'BAA'], bins=50, label='Baa')
# sns.distplot(IG_moodys_data.loc[:,'AAA'], bins=50, label='Aaa')
# plt.xlabel('Baa (blue), Aaa (orange)')
# Baa_quantile = IG_moodys_data.loc[:,'BAA'].rank(pct=True)[-1]
# Aaa_quantile = IG_moodys_data.loc[:,'AAA'].rank(pct=True)[-1]

# print("Moody's Baa yields of " + '{:.1%}'.format(.01*IG_moodys_data.loc[:,'BAA'][-1]) + " are higher than " + '{:.1%}'.format(Baa_quantile) + " of history (1919-current)")
# print("Moody's Aaa yields of " + '{:.1%}'.format(.01*IG_moodys_data.loc[:,'AAA'][-1]) + " are higher than " + '{:.1%}'.format(Aaa_quantile) + " of history (1919-current)")
# #print("1yr. forward yield change from this level is typically: ")

