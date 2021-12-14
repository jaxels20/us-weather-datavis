from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import functions as func

city_list = ['NYC', 'HOU', 'CLT', 'CQT', 'IND', 'JAX', 'MDW', 'PHL', 'PHX', 'SEA']

df_weather, df_placement = func.retrieve_data(city_list)

print(df_weather)
# dff = df_weather[df_weather['city'] == 'SEA']
# print(dff)