# -*- coding: utf-8 -*-
"""
Macro PCA:
Objective: Identify high-level drivers of movement in a collection of macro-sensitive tradable securities
outputs: PCA loadings, time-series of factor movements
todo: try with fractionally differenced series because why not
    -Find stationary series for factor 1 and adjust risk appetite accordingly
    -Find trends for all factors, invest in alighment with trends
    .
    -

"""

#import required models
import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

#set tickers for data gathering, collect data
#test_stocks = ['SPY', 'TLT', 'IEF','XLU','IGV','QQQ','GLD','GDX','MBB','XBI','MOO','TIP','EEM','UUP']
test_stocks = ['SPY','QQQ','TLT','IEF','SHY','TIP','AGG','LQD','IWM','IVW','IVE','IYF','IYE','IYM']
tickerData = {}
tickerDF = {}

for ticker in test_stocks:
    tickerData[ticker] = yf.Ticker(ticker)
    #get the historical prices for this ticker
    tickerDF[ticker] = tickerData[ticker].history(period='1d', start='2000-1-1', end='2020-12-31')

#choose column on which to run PCA, organize a historical table for analysis
test_col = 'Close'
pca_data = pd.DataFrame(columns=test_stocks)
for ticker in test_stocks:
    pca_data.loc[:,ticker] = tickerDF[ticker].loc[:,test_col]

#diagnostic - see when your series begin
for ticker in test_stocks:
    print(ticker , " " , tickerDF[ticker].index[1])

#create pca form sklearn and run it on outrights
pca = PCA(n_components=len(test_stocks)-1)

test_data = pca_data.dropna()

outright_pca = pca.fit(test_data)
outright_loadings = outright_pca.components_
outright_variances = outright_pca.explained_variance_
outright_stdev = np.sqrt(outright_variances)

#for i in range(0,outright_loadings.shape[0]):
for i in range(0,5):
    fig = plt.figure(figsize=(16,9), dpi=300)
    fig.suptitle(('Macro PCA loadings: factor ' + str(i+1)))
    sns.barplot(x=test_stocks,y=outright_loadings[i])


outright_time_series = pd.DataFrame(outright_pca.transform(test_data), index=test_data.index)
outright_time_series.columns = outright_time_series.columns+1
fig = plt.figure(figsize=(16,9), dpi=300)
time_plot = sns.lineplot(data=outright_time_series, dashes=False)

fig = plt.figure(figsize=(16,9), dpi=300)
time_plot = sns.lineplot(data=outright_time_series.iloc[:,1:], dashes=False)

