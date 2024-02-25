#After running the setup code, copy this code into another box, I tried to display a Sentinel image in a specific band but it only displays a white image

import folium
from IPython.display import Image

# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name = name,
    overlay = True,
    control = True
  ).add_to(self)

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Define your AOI
geoJSON = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -3.2275984231436894,
              15.131415167131749
            ],
            [
              -3.2275984231436894,
              15.09579432760799
            ],
            [
              -3.179786012280232,
              15.09579432760799
            ],
            [
              -3.179786012280232,
              15.131415167131749
            ],
            [
              -3.2275984231436894,
              15.131415167131749
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}

coords = geoJSON['features'][0]['geometry']['coordinates']
aoi = ee.Geometry.Polygon(coords)

ffa_db = ee.Image(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                       .filterBounds(aoi) 
                       .filterDate(ee.Date('2020-08-01'), ee.Date('2020-08-31')) 
                       .first() 
                       .clip(aoi))

url = ffa_db.select('B4').getThumbURL({'min': -20, 'max': 0})
disp.Image(url=url, width=800)

my_map = folium.Map(location=[15.113, -3.203], zoom_start=12)

my_map.add_ee_layer(ffa_db, {'min': -20, 'max': 0, 'bands': ['B4']}, 'Sentinel-2 Image')

my_map