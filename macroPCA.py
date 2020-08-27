# -*- coding: utf-8 -*-
"""
Macro PCA:
Objective: Identify high-level drivers of movement in a collection of macro-sensitive tradable securities
outputs: PCA loadings, time-series of factor movements
todo: try with fractionally differenced series because why not
    -Find stationary series for factor 1 and adjust risk appetite accordingly
    -Find trends for all factors, invest in alighment with trends
    -rename to generalize
    -

"""

#import required models
import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

import fracDiffTest as frac


class MacroPCA:
    
    def __init__(self, test_stocks):
        #set tickers for data gathering, collect data
        #test_stocks = ['SPY', 'TLT', 'IEF','XLU','IGV','QQQ','GLD','GDX','MBB','XBI','MOO','TIP','EEM','UUP']
        self.test_stocks = test_stocks;
        self.tickerData = {}
        self.tickerDF = {}
        
        print('retrieving data...')
        for ticker in self.test_stocks:
            self.tickerData[ticker] = yf.Ticker(ticker)
            #get the historical prices for this ticker
            self.tickerDF[ticker] = self.tickerData[ticker].history(period='1d', start='2000-1-1', end='2020-12-31')
        
        #choose column on which to run PCA, organize a historical table for analysis
        print('collating.')
        self.test_col = 'Close'
        self.pca_data = pd.DataFrame(columns=self.test_stocks)
        for ticker in self.test_stocks:
            self.pca_data.loc[:,ticker] = self.tickerDF[ticker].loc[:,self.test_col]
        
        #diagnostic - see when your series begin
        print('\ndata start dates:')
        for ticker in self.test_stocks:
            print(ticker , " " , self.tickerDF[ticker].index[1])
        
        #create pca form sklearn and run it on outrights
        print('\ncreating sklearn PCA')
        self.pca = PCA(n_components=len(self.test_stocks)-1)
        
        self.test_data = self.pca_data.dropna()
        
        self.outright_pca = self.pca.fit(self.test_data)
        self.outright_loadings = self.outright_pca.components_
        self.outright_variances = self.outright_pca.explained_variance_
        self.outright_stdev = np.sqrt(self.outright_variances)
        
        
    def loading_plots(self):
        #for i in range(0,outright_loadings.shape[0]):
        for i in range(0,5):
            fig = plt.figure(figsize=(16,9), dpi=300)
            fig.suptitle(('Macro PCA loadings: factor ' + str(i+1)))
            sns.barplot(x=self.test_stocks,y=self.outright_loadings[i])
        
    def factor_series(self):
        outright_time_series = pd.DataFrame(self.outright_pca.transform(self.test_data), index=self.test_data.index)
        outright_time_series.columns = outright_time_series.columns+1
        return outright_time_series
        
    def time_series_plots(self):
        outright_time_series = self.factor_series() 
        fig = plt.figure(figsize=(16,9), dpi=300)
        fig.suptitle('All Factor Time Series')
        sns.lineplot(data=outright_time_series, dashes=False)
        
        fig = plt.figure(figsize=(16,9), dpi=300)
        fig.suptitle('Time Series Excluding PCA Factor 1')
        sns.lineplot(data=outright_time_series.iloc[:,1:], dashes=False)
        
    def load_fractional_dimensions(self, filename):
        dimensionFile = open(filename, 'rb')
        self.fracional_dims = pickle.load(dimensionFile)
        dimensionFile.close()
        return self.fractional_dims

    def scan_store_dimensions(self, window, filename):
        dimensionFile = open(filename, 'wb')
        self.fractional_dims = {}
        test_data = self.factor_series()
        for column in test_data:
            self.fractional_dims[column] = frac.fracDiffOpt(test_data, column, window, .9, 50, .001, 1000)
        pickle.dump(self.fractional_dims, dimensionFile)
        dimensionFile.close()
        return self.fractional_dims

    def trading_ranges(self):
        signal = {}
        signal_percentile={}
        pca_data = self.factor_series()
        
        for column in pca_data.columns:
                input_table = (frac.fracDiff(tickerDF[ticker], 'logPx', dimensions_month[1][ticker], 30, 200)[0])#[-200:]
                signal[ticker] = ((input_table - input_table.rolling(30).mean())/input_table.rolling(30).std()).dropna()
                signal_percentile[ticker] = signal[ticker].rank(pct=True)
    
