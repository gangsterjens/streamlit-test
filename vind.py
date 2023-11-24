import requests
import json
import pandas as pd
import os
import ast
client_id = '9d4a669c-ad20-4ebe-9e0c-8c82b39a22ec'

def _get_stations(lon, lat, client_id, n_stations=5):
  endpoint = 'https://frost.met.no/sources/v0.jsonld?geometry=nearest(POINT({}%20{}))&nearestmaxcount={}&fields=id%2C%20name%2C%20distance%2C%20geometry'
  r = requests.get(endpoint.format(lon, lat, n_stations), auth=(client_id,''))
  json = r.json()
  json_list = json['data']
  station_list = []
  for i in json_list:
    station_id = i['id']
    name = i['name']
    distance = i['distance']
    lat = i['geometry']['coordinates'][0]
    lon = i['geometry']['coordinates'][1]
    station_list.append([station_id, name,  distance, lat, lon])
  return station_list

def _get__wind_observation(station_id, combined_date, wind=False, rain=False):
  endpoint = 'https://frost.met.no/observations/v0.jsonld'
  element_list = []
  vind = 'max(wind_speed_of_gust P1D)'
  regn = 'sum(precipitation_amount P1D)'
  if wind:
    element_list.append(vind)
  if rain:
    element_list.append(regn)
  parameters = {
        'sources': station_id,
        'elements': element_list,
        'referencetime': combined_date # row['Combined_Date']
    }

  r = requests.get(endpoint, parameters, auth=(client_id,''))
  if r.status_code == 200:
    json = r.json()
    json = json['data'][0]
    id = json['sourceId'].split(':')[0]
    json = json['observations'][0]
    value = json['value']
    elev = json['level']['value']
    returned_list = [id, value, elev]
    return returned_list
  else:
    return None

def get_weather_data(lat, lon, client_id, date, wind=False):
  stations = _get_stations(lat, lon, client_id)
  observations_list = []
  for station in stations:
    data = _get__wind_observation(station, date, wind)
    if data:
      observations_list.append(data)
  
  a = pd.DataFrame(stations, columns =['station_id', 'name',  'distance', 'lat', 'lon'])
  b = pd.DataFrame(observations_list, columns=['station_id', 'value', 'hoyde'])
  return pd.merge(a, b, left_on='station_id', right_on='station_id')

## df = get_weather_data(16.85264, 68.35646, client_id, '2023-02-09', wind=True)
st.text("test")
st.map(df)
