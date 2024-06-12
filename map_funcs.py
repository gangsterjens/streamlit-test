import folium
from streamlit_folium import st_folium

def folium_map(latitude, longitude, width=725):
    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker(
        [latitude, longitude], popup="hus", tooltip="Hus 7.8 moh"
    ).add_to(m)
    folium.Marker(
        [63.27373, 9.83214], popup="vann", tooltip="Vann 7.0 moh"
    ).add_to(m)

    return st_folium(m, width=width, returned_objects=[])
