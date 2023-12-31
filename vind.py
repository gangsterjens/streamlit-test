import requests
import json
import pandas as pd
import os
import ast
import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium
#locale
import weather_funcs as wf
import map_funcs as mf
import water_station as ws

st.set_option('deprecation.showPyplotGlobalUse', False)

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
    avstand_vann = int(float(gdf_list[6]) * 1000)
    st.markdown(f"Nærmeste vann er {avstand_vann} meter unna" )
    map_df = pd.DataFrame(gdf_list[4:6], columns=['lon', 'lat'])
    st.markdown("## Kart over skadested")
    mf.folium_map(float(latitude), float(longitude))
    fig = ws.get_water_graph(float(latitude), float(longitude), str(periode))
    st.markdown("## Vannstand 15 dager før t.o.m skadedato")
    st.pyplot(fig)
    

