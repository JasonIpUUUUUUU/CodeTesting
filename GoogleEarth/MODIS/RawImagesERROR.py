# I tried to download a raw image using the code from the website as a base but it outputs a white image, I am still trying to find out the reason

#defining the raw image collection
rw = ee.ImageCollection("LANDSAT/LC08/C02/T1")

# Initial date of interest (inclusive).
i_date = '2016-01-01'

# Final date of interest (exclusive).
f_date = '2020-01-01'

#selecting the RGB bands
rw = rw.select(['B4', 'B3', 'B2']).filterDate(i_date, f_date)

# Define the rural location of interest as a point away from the city.
r_lon = 5.175964
r_lat = 45.574064
r_poi = ee.Geometry.Point(r_lon, r_lat)

# Define a region of interest with a buffer zone of 1000 km around Lyon.
roi = r_poi.buffer(10000)

rw_img = rw.mean()

# Create a URL to the styled image for a region around France.
url = rw_img.getThumbUrl({
    'min': 10, 'max': 30, 'dimensions': 512, 'region': roi,})
print(url)

print('\nPlease wait while the thumbnail loads, it may take a moment...')
Image(url=url)


link = lst_img.getDownloadURL({
    'scale': 30,
    'crs': 'EPSG:4326',
    'fileFormat': 'GeoTIFF',
    'region': roi})
print(link)