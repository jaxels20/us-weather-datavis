from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import functions as func
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go






city_list = ['NYC', 'HOU', 'CLT', 'CQT', 'IND', 'JAX', 'MDW', 'PHL', 'PHX', 'SEA']

df_weather, df_placement = func.retrieve_data(city_list)
pd.set_option('display.max_columns', None)
df_HOU = df_weather[df_weather['city'] == 'HOU']
df_NYC = df_weather[df_weather['city'] == 'NYC']



a = [1,2,3,4]

print(tuple(a))