# -*- coding: utf-8 -*-
"""
ToDo: Create consolidated folder
        -capture last pca trend reversals
        -what is the optimum speed for predicting changes over 1wk/1mo
        -international PCA
        
Master file for market analytics.
#-run macro analysis for gdp prediction
#-run return estimation for rates and equities
-call the macro PCA, plot exposures
-plot time series of macro PCA
#-calculate trends of macro signals
#-calculate stationary signals of macro time series to identify stretched exposures
#-calculate trends of trading assets
#-calculate stationary short and long term series for trading assets

#-run hurst analysis(definitely needs work)
#-run volatility analysis (needs improvement)


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

import trendTest as trend
import macroPCA as macro

macro_tickers = ['SPY','QQQ','TLT','IEF','SHY','TIP','AGG','LQD','IWM','IVW','IVE','IYF','IYE','IYM']
macro_pca = macro.MacroPCA(macro_tickers)
macro_pca.loading_plots()
pca_series = macro_pca.factor_series()
macro_pca.time_series_plots()

pca_trend = {}
pca_trend_kza = {}
for column in pca_series.columns:
    [pca_trend[column], pca_trend_kza[column]] = trend.kza_filter(pca_series.loc[:,column].values, 100, 3)
    
    
#plot relevant pc's with trend information probably better to loop given that I added them all
fig = plt.figure(figsize=(16,9), dpi=300)
fig.suptitle(('Filtered PC1 Trend with last increment: ' + "%.3f"%(pca_trend_kza[1][-1] - pca_trend_kza[1][-2]) ))
sns.lineplot(x= pca_series.index, y=pca_trend_kza[1])

fig = plt.figure(figsize=(16,9), dpi=300)
fig.suptitle(('Filtered PC2 Trend with last increment: ' + "%.3f"%(pca_trend_kza[2][-1] - pca_trend_kza[2][-2]) ))
sns.lineplot(x= pca_series.index, y=pca_trend_kza[2])

fig = plt.figure(figsize=(16,9), dpi=300)
fig.suptitle(('Filtered PC3 Trend with last increment: ' + "%.3f"%(pca_trend_kza[3][-1] - pca_trend_kza[3][-2]) ))
sns.lineplot(x= pca_series.index, y=pca_trend_kza[3])

fig = plt.figure(figsize=(16,9), dpi=300)
fig.suptitle(('Filtered PC4 Trend with last increment: ' + "%.3f"%(pca_trend_kza[4][-1] - pca_trend_kza[4][-2]) ))
sns.lineplot(x= pca_series.index, y=pca_trend_kza[4])

fig = plt.figure(figsize=(16,9), dpi=300)
fig.suptitle(('Filtered PC5 Trend with last increment: ' + "%.3f"%(pca_trend_kza[5][-1] - pca_trend_kza[5][-2]) ))
sns.lineplot(x= pca_series.index, y=pca_trend_kza[5])


#scan dimensions for 30 day and 90 days (note return value is just for checking, state is stored in object)
#dimensions = macro_pca.scan_store_dimensions(30,'macro_dimensions_30.obj')
#dimensions = macro_pca.scan_store_dimensions(90,'macro_dimensions_90.obj')

#load dimensions if you don't want to recalculate (note return value is just for checking, state is stored in object)
load_dimensions = macro_pca.load_dimensions('macro_dimensions_30.obj')

# pca_range_signal = {}
# for column in pca_series.columns:
#     pca_range_signal = 