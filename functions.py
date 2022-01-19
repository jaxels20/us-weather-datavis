import pandas as pd

def retrieve_data(city_list):
    list_of_dfs = []
    for city in city_list:
        df_city = pd.read_csv(f'data\K{city}.csv')
        df_city['city'] = city
        list_of_dfs.append(df_city)
    df_weather = pd.concat(list_of_dfs, axis=0, ignore_index= True)

    # city, lat, lon
    placement = [['NYC', 40.730610, -73.935242],
                 ['HOU', 29.749907, -95.358421],
                 ['CLT', 35.227085, -80.843124],
                 ['CQT', 46.719663788, -92.455664844],
                 ['IND', 39.791000, -86.148003],
                 ['JAX', 30.332184, -81.655647],
                 ['MDW', 33.7446861, -117.9863236],
                 ['PHL', 39.952583, -75.165222],
                 ['PHX', 33.448376, -112.074036],
                 ['SEA', 47.608013, -122.335167]]
    df_placement = pd.DataFrame(placement, columns= ['city', 'lat', 'lon'])
    df_placement['extreme'] = float(0)
    df_placement['opacity'] = float(1)
    df_placement['size'] = 25

    df_weather['actuel_min_to_record_min'] = abs(df_weather['actual_min_temp'] - df_weather['record_min_temp'])
    df_weather['actuel_max_to_record_max'] = abs(df_weather['actual_max_temp'] - df_weather['record_max_temp'])

    df_weather['most_extreme'] = df_weather[['actuel_min_to_record_min', 'actuel_max_to_record_max']].min(axis=1)
    for i, row_city in enumerate(df_placement['city']):
        avg = df_weather[df_weather['city'] == row_city]['most_extreme'].mean()
        df_placement.at[i, 'extreme'] = avg



    return df_weather, df_placement


def checkbox_options():
    list = [
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Houston', 'value': 'HOU'},
        {'label': 'Charlotte', 'value': 'CLT'},
        {'label': 'Cloquet', 'value': 'CQT'},
        {'label': 'Indianapolis', 'value': 'IND'},
        {'label': 'Jacksonville', 'value': 'JAX'},
        {'label': 'Midway City', 'value': 'MDW'},
        {'label': 'Philadelphia', 'value': 'PHL'},
        {'label': 'Phoenix', 'value': 'PHX'},
        {'label': 'Seattle', 'value': 'SEA'}
     ]
    return list





