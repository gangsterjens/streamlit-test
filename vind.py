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
  st.markdown("## sett inn Koordinater")
  longitude = st.text_input("Lon", placeholder='16.85264')        
  latitude = st.text_input("Latitude", placeholder='68.35646')
  st.selectbox("Type naturskade", ["Storm", "Flom"])
  periode = st.date_input('Dag/Periode', "today")
  kjoyr = st.button("kjøyr")
if kjoyr:
  st.markdown(periode)
  df = wf.get_weather_data(longitude, latitude, client_id, periode, wind=True)
  ## st.text("test")
  col1, col2 = st.columns([5,1])
  col1.map(df)
  
  for index, row in df.iterrows():
    col2.metric(row['name'], row['value'])

  st.dataframe(df)

