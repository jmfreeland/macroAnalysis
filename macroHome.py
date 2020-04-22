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
gdp_plot = gdp_data[1]
gdp_chg_plot = gdp_data[1].diff(periods=3)


app.layout = html.Div(children=[
    html.H1(children='Macro Framework 0.00'),

    html.Div(children='''
        Odin: Reading the runes of macro data.
    '''),

    dcc.Graph(
        id='main-gdp-graph',
        figure={
            'data': [
                {'x': gdp_plot.index, 'y': gdp_plot.values, 'type': 'bar', 'name': 'GDP'},
                {'x': gdp_chg_plot.index, 'y': gdp_chg_plot.values, 'type': 'bar', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP in 2015 Dollars'
            }
        }
    ),
    
    dcc.Graph(
        id='gdp-chg-graph',
        figure={
            'data': [
                {'x': gdp_chg_plot.index, 'y': gdp_chg_plot.values, 'type': 'bar', 'name': 'GDP YoY'},
            ],
            'layout': {
                'title': 'Real GDP Change'
            }
        }
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)