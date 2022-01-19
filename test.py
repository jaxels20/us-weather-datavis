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
df_placement['extreme'] = float(0)
df_placement['size'] = 40

df_weather['actuel_min_to_record_min'] = abs(df_weather['actual_min_temp'] - df_weather['record_min_temp'])
df_weather['actuel_max_to_record_max'] = abs(df_weather['actual_max_temp'] - df_weather['record_max_temp'])

df_weather['most_extreme'] = df_weather[['actuel_min_to_record_min', 'actuel_max_to_record_max']].min(axis=1)
for i, row_city in enumerate(df_placement['city']):
    avg = df_weather[df_weather['city'] == row_city]['most_extreme'].mean()
    df_placement.at[i,'extreme'] = avg





fig = px.scatter_mapbox(data_frame= df_placement,
                        lon='lon',
                        lat='lat',
                        zoom=3,
                        center={'lat': 40.686288, 'lon': -98.24587245247825},
                        custom_data=['city'],
                        hover_data= [],
                        color='extreme',
                        size= 'size',
                        text='city')
fig.update_layout(mapbox_style='open-street-map', margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.show()

fig1 = go.Figure(go.Scattermapbox(
    lat=df_placement['lat'],
    lon=df_placement['lon'],
    mode='markers+text',
    customdata=df_placement['city'],
    marker=go.scattermapbox.Marker(
        size=25,
        color=df_placement['extreme'],
        opacity=df_placement['opacity']
    ),
    text=df_placement['city'],
    textposition='top right',
    hoverinfo='text',
))