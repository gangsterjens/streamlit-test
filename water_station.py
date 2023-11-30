import requests
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
import json
import requests
from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic
from datetime import datetime, timedelta
api_key = '6hqaEMkYx0iv06elQS9wgA=='

headers = {
    'accept': 'application/json',
    'X-API-Key': api_key
}

# API docs : https://hydapi.nve.no/UserDocumentation/



def _show_water(data, marker='o', color='c', label=None, x_label='Dager før inntruffet dato', y_label='Vannstand (moh)', title=None, show_legend=True):
    """
    Plot data with optional customization.

    Parameters:
    data (list): A list of data points.
    marker (str, optional): Marker style for the plot. Default is 'o'.
    color (str, optional): Color for the plot. Default is 'b' (blue).
    label (str, optional): Label for the data series in the legend. Default is None.
    x_label (str, optional): Label for the x-axis. Default is None.
    y_label (str, optional): Label for the y-axis. Default is None.
    title (str, optional): Title for the plot. Default is None.
    show_legend (bool, optional): Whether to display the legend. Default is True.

    Returns:
    None

    The function plots the data and displays the plot using `plt.show()`.
    """
    # Handle empty or all-NaN data
    if len(data) == 0 or all(np.isnan(data)):
        print("No valid data to plot.")
        return
    plt.style.use('fivethirtyeight')
    # Correcting the interpolation process
    valid_indices = np.arange(len(data))[~np.isnan(data)]
    valid_values = np.array(data)[~np.isnan(data)]
    interpolated_data = np.interp(np.arange(len(data)), valid_indices, valid_values)
    x_list = list(range(-len(interpolated_data) + 1, 1))
    plt.figure(figsize=(10, 6), dpi=80)
    # Plotting
    plt.plot(x_list, interpolated_data, marker=marker, color=color, label=label)

    # Customize plot appearance
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if title:
        plt.title(title)
    if show_legend and label:
        plt.legend()

    plt.show()

# Example usage:
# plot_data([1.0, 2.0, None, 4.0, 5.0, None, 7.0], marker='x', color='r', label='Interpolated Data',
#           x_label='Time', y_label='Value', title='Interpolated Data Plot')


def _get_stations(lat, lon):
  # Få de aktive stasjonene
  url = 'https://hydapi.nve.no/api/v1/Stations?Active=OnlyActive'

  # Headers including the required API key
  headers = {
      'accept': 'application/json',
      'X-API-Key': api_key
  }

  r = requests.get(url, headers=headers)
  data = r.json()
  data = data['data']
  station_list = [] # etablere tom liste
  # plukke ut kun relevante felter fra listen med stasjoenr
  for i in data:
    id = i['stationId']
    st_lat = i['latitude']
    st_lon = i['longitude']
    status = i['stationStatusName']
    rivername = i['riverName']
    maleenheter = []
    for el in i['seriesList']:
      maleenheter.append(el['parameterName'])

    station_list.append([id, st_lat, st_lon, status, rivername, maleenheter])
    # hente kun de som har vannstand-måling
  station_list2 = []
  for station in station_list: # Station er list.
    if ('Vannstand' in station[-1]): #Station[-1] er en liste med med elementer som måles på stationen.
      station_list2.append(station)

    # Finne nærmeste stasjon

  df_st = pd.DataFrame(station_list2, columns=['station_id', 'lat', 'lon', 'status', 'name', 'measurements']) # etablere en dataframe som kan sorteres

  house = (lon, lat)
  df_st['station_point'] = list(zip(df_st['lon'], df_st['lat']))

  # Function to calculate distance
  def _calculate_distance(station_point):
      return geodesic(station_point, house).kilometers

  # Apply the function to each row
  df_st['avstand'] = df_st['station_point'].apply(_calculate_distance)

  df_st = df_st.sort_values('avstand').head(5).reset_index()
  return df_st

# _get_stations(60.423515, 10.05877) # TEST 


def _get_water_station_data(station_id, inntruffet_dato):
  prior_date = (datetime.strptime(inntruffet_dato, '%Y-%m-%d') - timedelta(days=15)).strftime('%Y-%m-%d')

  parameters = '1000'
  url = f'https://hydapi.nve.no/api/v1/Observations?StationId={station_id}&Parameter={parameters}&ResolutionTime=1440&ReferenceTime={prior_date}/{inntruffet_dato}'
  r = requests.get(url, headers=headers)
  data = r.json()
  plot_list = []
  for el in data['data'][0]['observations']:
    plot_list.append(el['value'])
  return _show_water(plot_list)
# _get_water_station_data(df_test.iloc[0]['station_id'], inntruffet_dato) TEST


def get_water_graph(lat, lon, inntruffet_dato):
  df_temp = _get_stations(lat, lon)
  temp_station_id = df_temp.iloc[0]['station_id']
  plot = _get_water_station_data(temp_station_id, inntruffet_dato)
  return plot
