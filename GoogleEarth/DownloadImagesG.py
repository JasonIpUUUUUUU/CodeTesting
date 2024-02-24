import ee
from datetime import datetime

# Initialize the Earth Engine API
ee.Initialize()

# Define the region of interest (ROI)
roi = ee.Geometry.Point([-122.4439, 37.7538])  # Example location (longitude, latitude)

# Define time range
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 31)

# Create a Landsat image collection
landsat_collection = (ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
                      .filterBounds(roi)
                      .filterDate(ee.Date(start_date), ee.Date(end_date))
                      .sort('CLOUDY_PIXEL_PERCENTAGE')
                      .first())

# Print the image information
print('Landsat Image Information:', landsat_collection.getInfo())

# Download the image
download_config = {
    'scale': 30,
    'region': roi
}

task = ee.batch.Export.image.toDrive(
    image=landsat_collection,
    description='landsat_image',
    folder='earth_engine_images',
    scale=30
)

# Start the export task
task.start()