# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:10:22 2020

@author: freel

todo: create spread analysis page, create vol analysis page
"""

import dash
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


import macroAnalysis

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

gdp_data = macroAnalysis.gdp_history()
[regression_list, comp_data, prediction_data, series_name, points_required, gdp_model] = macroAnalysis.scatter_data_gdp()

gdp_plot = gdp_data[1]
gdp_chg_plot = gdp_data[1].diff(periods=3)
heatmap_data = macroAnalysis.macro_heatmap()
[prediction_results, last_date] = macroAnalysis.prediction_outputs()

app.layout = html.Div(
    id='main-chart-block',
    style={'backgroundColor' : 'red'},
    children=[
   
    html.Div(id='gdp-graph-block', 
    style={'position' : 'absolute',
           'left' : '1%', 
           'width': '48%', 
           'height': '500px', 
           'top' : '20px'},
    children=
    dcc.Graph(
        id='main-gdp-graph',
        figure={
            'data': [
                {'x': gdp_plot.index,
                 'y': gdp_plot.values,
                 'marker' : {'color': gdp_plot.pct_change(), 
                             'colorscale': 'Greys',
                             'opacity': '0.8'},
                 'type': 'bar',
                 'name': 'GDP'}
                
            ],
            'layout': {
                'title': 'Real GDP in 2015 Dollars',
                'paper_bgcolor' : 'rgba(28,30,33,0.50)',
                'plot_bgcolor' : 'rgba(28,30,33,0.50)',
                'font' : {'color' : 'rgba(240,235,216,.9)'},
                'margin' : {'l': '50', 'r' : '50', 't' : '50', 'b' : '50' }
            }
        }
    )),
    
    html.Div(id='gdp-chg-graph-block', 
    style={'position' : 'absolute', 'width': '48%', 'height': '500px', 'top' : '20px' , 'left' : '51%'},
    children=
    dcc.Graph(
        id='gdp-chg-graph',
        figure={
            'data': [
                {'x': gdp_chg_plot.index, 'y': gdp_chg_plot.values, 'type': 'bar', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP Change',
                'plot_bgcolor' : 'rgba(28,30,33,0.50)',
                'paper_bgcolor' : 'rgba(28,30,33,0.50)',
                'font' : {'color' : 'rgba(240,235,216,.9)'},
                'margin' : {'l': '50', 'r' : '50', 't' : '50', 'b' : '50' }
            }
        }
    )),
    
    html.Div(id='gdp-heatmap-block', 
    style={'position' : 'absolute', 'width': '48%', 'left' : '1%', 'height': '500px', 'top' : '500px'},
    children=
    dcc.Graph(
        id='input-heatmap',
        figure={
            'data': [
                {'x': heatmap_data.columns, 
                 'y': heatmap_data.index, 
                 'z': heatmap_data.values,
                 'zmin' : -.03,
                 'zmax' : .03,
                 'type': 'heatmap', 
                 'colorscale' : 'Portland',
                 'reversescale' : True,
                 'name': 'GDP Input Heatmap'},
            ],
            'layout': {
                'title': 'GDP Input Heatmap ',
                'plot_bgcolor' : 'rgba(28,30,33,0.50)',
                'paper_bgcolor' : 'rgba(28,30,33,0.50)',
                'font' : {'color' : 'rgba(240,235,216,.9)'},
                'margin' : {'l': '50', 'r' : '50', 't' : '50', 'b' : '50' }
            }
        }
    )),  
    
    
    html.Div(id='gdp-scatter-block', 
    style={'position' : 'absolute', 'width': '48%', 'height': '500px', 'top' : '500px' , 'left' : '51%'},
    children=
    dcc.Graph(
        id='gdp-scatter-graph',
        figure={
            'data': [
                {'x': prediction_data['PCEC96'].loc[:,'PCEC96'].values, 'y': prediction_data['PCEC96'].loc[:,'realGDP'].values, 'type': 'scatter', 'mode' : 'markers', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP Change vs. ',
                'plot_bgcolor' : 'rgba(28,30,33,0.50)',
                'paper_bgcolor' : 'rgba(28,30,33,0.50)',
                'font' : {'color' : 'rgba(240,235,216,.9)'},
                'margin' : {'l': '50', 'r' : '50', 't' : '50', 'b' : '50' }
            }
        }
    )),
    
    html.Div(id='prediction-bar-block', 
    style={'position' : 'absolute', 'width': '48%', 'height': '500px', 'top' : '1000px' , 'left' : '1%'},
    children=
    dcc.Graph(
        id='prediction-bar-graph',
        figure={
            'data': 
                [{'x': prediction_results.index,
                 'y': prediction_results.iloc[:,0].values.tolist(),
                 'type': 'bar', 
                 'marker' : {'color': (np.datetime64('today') - pd.Series(list(last_date.values()))).dt.days, 
                             'colorscale': 'Greys',
                             'cmin' : 30,
                             'cmax' : 180,
                             'showscale' : True,
                             'reversescale' : True,      
                             'name': 'Predicted GDP'
                             }}],
            'layout': {
                'title': 'Real GDP Change vs. ',
                'plot_bgcolor' : 'rgba(28,30,33,0.50)',
                'paper_bgcolor' : 'rgba(28,30,33,0.50)',
                'font' : {'color' : 'rgba(240,235,216,.9)'},
                'margin' : {'l': '50', 'r' : '50', 't' : '50', 'b' : '50' }
            }
        }
    )) 

    
])

if __name__ == '__main__':
    app.run_server(debug=True)