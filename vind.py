import requests
import json
import pandas as pd
import os
import ast
import streamlit as st
import datetime
import weather_funcs as wf
import folium
from streamlit_folium import st_folium


########################################################################################################################
# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=725, returned_objects=[])
########################################################################################################################

client_id = '9d4a669c-ad20-4ebe-9e0c-8c82b39a22ec'

st.markdown("# Naturskadedata")
with st.sidebar:
    st.markdown("## sett inn Koordinater")
    longitude = st.text_input("Lon", placeholder='16.85264')        
    latitude = st.text_input("Latitude", placeholder='68.35646')
    periode = st.date_input('Dag/Periode', "today")
    type_naturskade = st.selectbox("velg naturskade", ["Flom", "Storm"])
    kjoyr = st.button("kjøyr")
## Dashboard for stormdata:
if kjoyr and (type_naturskade == 'Storm'):
  st.markdown(periode)
  df = wf.get_weather_data(longitude, latitude, client_id, periode, wind=True)
  ## st.text("test")
  col1, col2 = st.columns([5,1])
  col1.map(df)
  for index, row in df.iterrows():
    col2.metric(row['name'], row['value'])
  st.dataframe(df)  
# Dashboard for flomdata: 
elif kjoyr and (type_naturskade == 'Flom'):
    st.markdown("Skadedata fra flom")
    gdf_list = wf.find_water(float(longitude), float(latitude), distance=1000)
    st.markdown(gdf_list)
    map_df = pd.DataFrame(gdf_list[4:6], columns=['lon', 'lat'])
    st.map(map_df, zoom=15, size=3)

