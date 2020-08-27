# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 17:41:14 2020

@author: freel
"""

import pandas as pd
import numpy as np
import math
import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
kza = importr("kza")
import matplotlib.pyplot as plt


# trend_signal = {}
# plt.figure(figsize = (900,900), dpi=300)
# for ticker in test_stocks:
#     trend_signal[ticker ] = trend_test(tickerDF[ticker].loc[:,'Close'],90)


def trend_test(test_data, trend_filter):
        
    points = test_data.shape[0]
    period_change = pd.DataFrame()

    i=1
    test_point = int(points/i)

    while(test_point>1):
        period_change.loc[test_point,'Difference'] = test_data[-1] - test_data[-test_point]
        i+=1    
        test_point = int(points/i)

    plt.plot(period_change)
    return period_change.loc[period_change.index<trend_filter,'Difference'].sum()

def kza_filter(test_data, window, iterations):
    kz_output = kza.kz(robjects.FloatVector(test_data), window, iterations)
    kza_output=kza.kza(robjects.FloatVector(test_data), window, rpy2.rinterface.NULL, iterations)
    return np.array(kz_output), np.array(kza_output[1])

    