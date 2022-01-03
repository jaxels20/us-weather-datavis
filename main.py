from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import functions as func
import plotly.graph_objects as go
from plotly.subplots import make_subplots



city_list = ['NYC', 'HOU', 'CLT', 'CQT', 'IND', 'JAX', 'MDW', 'PHL', 'PHX', 'SEA']
selected_cities1 = []
selected_cities2 = []
colors = ['aqua', 'darksalmon', 'grey', 'red', 'yellow']


df_weather, df_placement = func.retrieve_data(city_list)

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )

app.layout = html.Div(
    [html.H1('Visualisation of the weather in the US in the year 2015'), dbc.Row(
    dbc.Col(
    dcc.Graph(id = 'map', figure = {'layout': {

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
                            center={'lat': 40.686288, 'lon': -98.24587245247825},
                            custom_data=['city']
                            )
    fig.update_layout(mapbox_style='open-street-map')
    return fig




@app.callback(
    Output(component_id='subgraph1', component_property='figure'),
    Input(component_id='map', component_property='clickData')
)
def generate_subgraph(clickdata):
    bool = True
    if clickdata is not None:
        clicked_city = clickdata['points'][0]['customdata'][0]
        if clicked_city in selected_cities1:
            selected_cities1.remove(clicked_city)
        else:
            selected_cities1.append(clicked_city)

        dff = df_weather[df_weather['city'].isin(selected_cities1)]

        final_fig = make_subplots(rows=len(selected_cities1), cols=1, shared_xaxes=False, shared_yaxes=True, subplot_titles=tuple(selected_cities1) )
        final_fig.update_layout(height=450 * len(selected_cities1)
        )

        for i, city in enumerate(selected_cities1, 1):
            if bool:
                #temp that day all time high/low:
                final_fig.add_trace(go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['record_min_temp'], mode='lines', line_color='indigo', fill=None, showlegend=False), col=1, row=i)
                final_fig.add_trace(go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['record_max_temp'],mode='lines', line_color='indigo', fill='tonexty', name= 'Span of min and max temperature ever recorded'), col=1, row=i)

                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['actual_mean_temp'], mode='lines', line_color='black', name='Average temperature'), col=1, row=i)
                #all time average temp that day:
                final_fig.add_trace(go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['average_min_temp'], mode='lines', line_color='blue', fill=None, showlegend=False), col=1, row=i)
                final_fig.add_trace(go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['average_max_temp'],mode='lines', line_color='blue', fill='tonexty', name='Span of average min and max temperature every year'), col=1, row=i)
                bool = False
            else:
                # temp that day all time high/low:
                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['record_min_temp'],
                               mode='lines', line_color='indigo', fill=None, showlegend=False), col=1, row=i)
                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['record_max_temp'],
                               mode='lines', line_color='indigo', fill='tonexty',
                               name='Span of min and max temperature ever recorded', showlegend=False), col=1, row=i)

                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['actual_mean_temp'],
                               mode='lines', line_color='black', name='Average temperature', showlegend=False), col=1, row=i)
                # all time average temp that day:
                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['average_min_temp'],
                               mode='lines', line_color='blue', fill=None, showlegend=False), col=1, row=i)
                final_fig.add_trace(
                    go.Scatter(x=dff[dff['city'] == city]['date'], y=dff[dff['city'] == city]['average_max_temp'],
                               mode='lines', line_color='blue', fill='tonexty',
                               name='Span of average min and max temperature every year', showlegend=False), col=1, row=i)


        final_fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        #labels:
        for i in range(1, len(selected_cities1)+1):
            final_fig['layout'][f'yaxis{i}']['title'] = 'Temperature in fahrenheit'
            final_fig['layout'][f'xaxis{i}']['title'] = 'Date'



        return final_fig
    return px.scatter()

@app.callback(
    Output(component_id='subgraph2', component_property='figure'),
    Input(component_id='map', component_property='clickData')
)
def generate_subgraph(clickdata):
    if clickdata is not None:
        clicked_city = clickdata['points'][0]['customdata'][0]
        if clicked_city in selected_cities2:
            selected_cities2.remove(clicked_city)
        else:
            selected_cities2.append(clicked_city)

        dff = df_weather[df_weather['city'].isin(selected_cities2)]

        fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], shared_xaxes=True)

        for i, city in enumerate(selected_cities2):
            fig.add_trace(go.Box(x=dff[dff['city'] == city]['actual_mean_temp'], name=city, legendgroup='1', marker=dict(color=colors[i])),
                          row=1, col=1)
            hist_fig = go.Histogram(x=dff[dff['city'] == city]['actual_mean_temp'], name=city, marker= dict(opacity=0.70, color=colors[i]), legendgroup='1', showlegend=False)

            fig.add_trace(hist_fig, row=2, col=1)


        fig.layout['barmode'] = 'overlay'
        fig['layout']['xaxis2']['title'] = 'Average temperature in fahrenheit'
        fig['layout']['yaxis2']['title'] = 'Frequency'
        fig.update_layout(title_text='Distribution of average temperature')

        return fig
    return px.histogram()

if __name__ == '__main__':
    app.run_server(debug=True)