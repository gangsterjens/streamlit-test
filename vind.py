import requests
import json
import pandas as pd
import os
import ast
import streamlit as st
import datetime
import weather_funcs as wf
client_id = '9d4a669c-ad20-4ebe-9e0c-8c82b39a22ec'

st.markdown("# Naturskadedata")
with st.sidebar:
  storm_tab, flom_tab = st.tabs(['Storm', 'Flom'])
  with storm_tab:
    st.markdown("## sett inn Koordinater")
    longitude = st.text_input("Lon", placeholder='16.85264')        
    latitude = st.text_input("Latitude", placeholder='68.35646')
    periode = st.date_input('Dag/Periode', "today")
    kjoyr_storm = st.button("kjøyr")
  with flom_tab:
    st.markdown("## sett inn Koordinater")
    longitude = st.text_input("Lon", placeholder='16.85264')        
    latitude = st.text_input("Latitude", placeholder='68.35646')
    periode = st.date_input('Dag/Periode', "today")
    kjoyr_storm = st.button("kjøyr")
    
    
    

if kjoyr_storm:
  st.markdown(periode)
  df = wf.get_weather_data(longitude, latitude, client_id, periode, wind=True)
  ## st.text("test")
  col1, col2 = st.columns([5,1])
  col1.map(df)
  for index, row in df.iterrows():
    col2.metric(row['name'], row['value'])

  st.dataframe(df)
if koyr_flom:
  gdf_list = find_water(lon, lat, distance)
  map_df = pd.DataFrame(gdf_list[4:6], columns=['lon', 'lat'])
  st.map(map_df)

