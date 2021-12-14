from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import functions as func
import plotly.graph_objects as go



city_list = ['NYC', 'HOU', 'CLT', 'CQT', 'IND', 'JAX', 'MDW', 'PHL', 'PHX', 'SEA']

df_weather, df_placement = func.retrieve_data(city_list)

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )

app.layout = html.Div([dbc.Row(
    dbc.Col(
    dcc.Graph(id = 'map', clickData= ['customdata'], figure={'layout': {
                                'height': 600,
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            }})
    , width=6)
    ),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='subgraph1')
            , width=6),
        dbc.Col(
            dcc.Graph(id='subgraph2')
            , width=6)
    ])
])

@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='map', component_property='clickData')
)
def generate_map(clickdata):
    fig = px.scatter_mapbox(data_frame= df_placement,
                            lon='lon',
                            lat='lat',
                            zoom=3,
                            center= {'lat' : 40.686288, 'lon': -98.24587245247825},
                            custom_data=['city']
                            )
    fig.update_layout(mapbox_style='open-street-map')
    return fig




@app.callback(
    Output(component_id='subgraph1', component_property='figure'),
    Input(component_id='map', component_property='clickData')
)
def generate_subgraph(clickdata):
    if type(clickdata) != list:
        clicked_city = clickdata['points'][0]['customdata'][0]
        dff = df_weather[df_weather['city'] == clicked_city]

        #fig = plt.bar(day_order, record_max_temps - record_min_temps, bottom=record_min_temps,
        #    edgecolor='none', color='#C3BBA4', width=1)
        fig = go.Figure()

        #temp that day all time high:
        fig.add_trace(go.Scatter(x=dff['date'], y=dff['record_min_temp'], mode='lines', line_color='indigo', fill=None))
        fig.add_trace(go.Scatter(x=dff['date'], y=dff['record_max_temp'],mode='lines', line_color='indigo', fill='tonexty'))

        fig1 = go.Figure()
        # fig.add_trace(
        #     go.Scatter(x=dff['date'], y=dff['actual_mean_temp'], mode='lines', line_color='blue', fill='tonexty'))
        #all time average temp that day:
        fig.add_trace(go.Scatter(x=dff['date'], y=dff['average_min_temp'], mode='lines', line_color='blue', fill=None))
        fig.add_trace(go.Scatter(x=dff['date'], y=dff['average_max_temp'],mode='lines', line_color='blue', fill='tonexty'))
        return fig
    return px.scatter()






if __name__ == '__main__':
    app.run_server(debug=False)