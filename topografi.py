import requests
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt


def create_tverssnitt(vlon, lon, vlat, lat, steps=10):

  def create_list(water_lat, house_lat, steps):
    diff = water_lat - house_lat
    punkt_list = []
    for x in range(0, steps + 1):
      diviser = x
      point = house_lat + (diff * diviser/steps)
      punkt_list.append(point)
    return punkt_list

  liste1 = create_list(vlon, lon, steps)
  liste2 = create_list(vlat, lat, steps)

  cords_liste = list(zip(liste1, liste2))

  hoyde_liste = []
  for cord in cords_liste:
    url = f'https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4258&nord={cord[1]}&ost={cord[0]}&geojson=false'
    response = requests.get(url)
    hoyde = response.json()['punkter'][0]['z']
    hoyde_liste.append(hoyde)


  

  y_line = 7.3  # The y-value for the horizontal line

  # Calculate y-axis limits
  y_min = min(hoyde_liste) * 0.8
  y_max = max(hoyde_liste) * 1.1

  # Create the plot
  plt.plot(hoyde_liste)

  # Fill the area underneath the line
  plt.fill_between(range(len(hoyde_liste)), y_line, color='blue', alpha=0.3)
  plt.fill_between(range(len(hoyde_liste)), hoyde_liste, color='brown', alpha=1)

  # Add horizontal line
  ## plt.hlines(y=y_line, xmin=0, xmax=len(hoyde_liste) - 1, color='blue', linestyle='--')

  # Add annotations
  plt.annotate('Hus', xy=(0, hoyde_liste[0]), xytext=(0, hoyde_liste[0] + 0.5),
              arrowprops=dict(facecolor='black', shrink=0.05))

  #plt.annotate('elvekant', xy=(len(hoyde_liste) - 2, hoyde_liste[-2]), xytext=(len(hoyde_liste) - 2, hoyde_liste[-2] ),
             # arrowprops=dict(facecolor='black', shrink=0.05))

  # Add titles and labels
  plt.title('Topografisk tversnitt')
  plt.xlabel('Avstand hus og vann')
  plt.ylabel('m.o.h')

  # Set y-axis limits
  plt.ylim(y_min, y_max)

  # Display the plot
  plt.show()

if __name__ == '__main__':
  lat = 63.27374
  lon = 9.83084
  vlat, vlon = 63.27373, 9.83214
  create_tverssnitt(vlon, lon, vlat, lat, 10)
