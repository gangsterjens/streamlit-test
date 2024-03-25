import requests
import json
import pandas as pd
import osmnx as ox
import pandas as pd
from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic



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
    coordinates = i['geometry']['coordinates']
    station_list.append([station_id, name,  distance, coordinates])
  return station_list


def _get_wind_observation(station_id, combined_date, wind=True, rain=False):
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

def get_weather_data(lat, lon, client_id, date, wind=False, rain=False):
  stations = _get_stations(lat, lon, client_id)
  observations_list = []
  for station in stations:
    data = _get_wind_observation(station, date, wind=wind)
    if data:
      observations_list.append(data)

  a = pd.DataFrame(stations, columns =['station_id', 'name',  'distance', 'coordinates'])
  b = pd.DataFrame(observations_list, columns=['station_id', 'value', 'hoyde'])
  df = pd.merge(a, b, left_on='station_id', right_on='station_id')
  def parse_coordinates(coord_string):
    coords_list = ast.literal_eval(coord_string)  # Parse string to list
    return {'longitude': coords_list[0], 'latitude': coords_list[1]}
  df[['longitude', 'latitude']] = df['coordinates'].apply(lambda x: pd.Series(parse_coordinates(x)))
  return df

# Apply the function to the DataFrame column
df[['longitude', 'latitude']] = df['coordinates'].apply(lambda x: pd.Series(parse_coordinates(x)))



#lon, lat = 10.273419,	60.174558
import osmnx as ox
import pandas as pd
from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic


def find_water(lon, lat, distance):
  tags = {'water': True,
          'waterway': True,
          'landuse': 'reservoir',
          'natural': ['bay', 'beach', 'blowhole', 'cape', 'coastline', 'crevasse', 'geyser', 'glacier', 'hot_spring', 'isthmus', 'mud', 'peninsula', 'reef', 'shingle', 'shoal', 'spring', 'strait', 'water', 'wetland'],
          'amenity': 'drinking_water'
          }
  try:
      gdf = ox.features_from_point((lat, lon), tags, dist=distance)
  except ValueError as ve:
      # Handle the ValueError exception here
      # You can also access the error message using ve.args
      return ['', '', '', '', '', '']


  row_values = []
  for index, row in gdf.iterrows():
    # find closest point
    house = Point(lon, lat)
    closest_point = nearest_points(house, row['geometry'])[1]
    closest_point2 = nearest_points(house, row['geometry'])
    # find distance
    cp_ll = (closest_point.x, closest_point.y)
    house_ll = (lon, lat)
    distance_km = geodesic(house_ll, cp_ll).kilometers
    try:
      name = row['name']
    except:
      name = ''
    try:
      waterway = row['waterway']
    except:
      waterway = ''
    try:
      natural = row['natural']
    except:
      natural = ''
    row_values.append([name, waterway, natural, cp_ll, house_ll, distance_km])
    df_tmp = pd.DataFrame(row_values, columns=['name', 'waterway', 'natural', 'cp_ll', 'house_ll', 'distance_km']).sort_values('distance_km').reset_index()
  return df_tmp.loc[0, :].values.flatten().tolist()
