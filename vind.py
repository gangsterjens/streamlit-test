import requests
import json
import pandas as pd
import os
import ast
import streamlit as st
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
    lon = i['geometry']['coordinates'][0]
    lat = i['geometry']['coordinates'][1]
    station_list.append([station_id, name,  distance, lon, lat])
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
  
  a = pd.DataFrame(stations, columns =['station_id', 'name',  'distance', 'lon', 'lat'])
  b = pd.DataFrame(observations_list, columns=['station_id', 'value', 'hoyde'])
  return pd.merge(a, b, left_on='station_id', right_on='station_id')

st.text("Naturskadedata")
with st.sidebar:
  st.text("sett inn Koordinater")
  longitude = st.text_input("Lon", placeholder='16.85264')        
  latitude = st.text_input("Latitude", placeholder='68.35646')
  st.selectbox("Type naturskade", ["Storm", "Flom"])
  kjoyr = st.button("kjøyr")
if kjoyr:
  df = get_weather_data(longitude, latitude, client_id, '2023-02-09', wind=True)
  ## st.text("test")
  col1, col2 = st.columns([5,1])
  col1.map(df)
  
  for index, row in df.iterrows():
    col2.metric(row['name'], row['value'])

  st.dataframe(df)

