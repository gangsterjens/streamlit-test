import folium
from streamlit_folium import st_folium

def folium_map(latitude, longitude, width=725):
    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker(
        [latitude, longitude]
    ).add_to(m)

    return st_folium(m, width=width, returned_objects=[])
