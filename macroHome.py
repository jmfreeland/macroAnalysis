# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:10:22 2020

@author: freel
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

import macroAnalysis

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

gdp_data = macroAnalysis.gdp_history()
[regression_list, comp_data, prediction_data, series_name, points_required, gdp_model] = macroAnalysis.scatter_data_gdp()

gdp_plot = gdp_data[1]
gdp_chg_plot = gdp_data[1].diff(periods=3)
heatmap_data = macroAnalysis.macro_heatmap()

app.layout = html.Div(children=[
   

   

    html.Div(id='gdp-graph-block', 
    style={'position' : 'absolute', 'width': '50%', 'height': '500px', 'top' : '20px'},
    children=
    dcc.Graph(
        id='main-gdp-graph',
        figure={
            'data': [
                {'x': gdp_plot.index, 'y': gdp_plot.values, 'type': 'bar', 'name': 'GDP'},
                {'x': gdp_chg_plot.index, 'y': gdp_chg_plot.values, 'type': 'bar', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP in 2015 Dollars',
                'paper_bgcolor' : 'rgba(0,0,0,0)',
                'plot_bgcolor' : 'rgba(0,0,0,0)',
                'margin' : {'l': '20', 'r' : '20', 't' : '20', 'b' : '20' }
            }
        }
    )),
    
    html.Div(id='gdp-chg-graph-block', 
    style={'position' : 'absolute', 'width': '50%', 'height': '500px', 'top' : '20px' , 'left' : '50%'},
    children=
    dcc.Graph(
        id='gdp-chg-graph',
        figure={
            'data': [
                {'x': gdp_chg_plot.index, 'y': gdp_chg_plot.values, 'type': 'bar', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP Change',
                'plot_bgcolor' : 'rgba(0,0,0,0)',
                'paper_bgcolor' : 'rgba(0,0,0,0)',
                'margin' : {'l': '20', 'r' : '20', 't' : '20', 'b' : '20' }
            }
        }
    )),
    
    html.Div(id='gdp-heatmap-block', 
    style={'position' : 'absolute', 'width': '50%', 'height': '500px', 'top' : '500px' , 'left' : '0%'},
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
                'plot_bgcolor' : 'rgba(0,0,0,0)',
                'paper_bgcolor' : 'rgba(0,0,0,0)',
                'margin' : {'l': '20', 'r' : '20', 't' : '20', 'b' : '20' }
            }
        }
    )),  
    
    
    html.Div(id='gdp-scatter-block', 
    style={'position' : 'absolute', 'width': '50%', 'height': '500px', 'top' : '500px' , 'left' : '50%'},
    children=
    dcc.Graph(
        id='gdp-scatter-graph',
        figure={
            'data': [
                {'x': prediction_data['PCEC96'].loc[:,'PCEC96'].values, 'y': prediction_data['PCEC96'].loc[:,'realGDP'].values, 'type': 'scatter', 'mode' : 'markers', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP Change vs. ',
                'plot_bgcolor' : 'rgba(0,0,0,0)',
                'paper_bgcolor' : 'rgba(0,0,0,0)',
                'margin' : {'l': '20', 'r' : '20', 't' : '20', 'b' : '20' }
            }
        }
    ))
    
    

    
])

if __name__ == '__main__':
    app.run_server(debug=True)