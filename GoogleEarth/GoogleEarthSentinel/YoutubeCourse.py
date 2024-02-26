# the following code exports sentinel images to your google drive, I learned how to do it from https://www.youtube.com/watch?v=Lqirs04EccA&t=51s

i_date = '2020-01-01'
f_date = '2020-05-01'

geometry = ee.Geometry.Point([31.5051, -26.6061])

location = geometry.coordinates().getInfo()[::-1]

s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
rgbVis = {
    'min': 0.0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2']
}

def maskS2clouds(image):
  qa = image.select('QA60')
  cloudBitMask = 1 << 10
  cirrusBitMask = 1 << 11
  mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
      qa.bitwiseAnd(cirrusBitMask).eq(0))
  return image.updateMask(mask) \
  .select("B.*") \
  .copyProperties(image,["system:time_start"])

filtered = s2.filter(ee.Filter.date(i_date, f_date)) \
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
  .filter(ee.Filter.bounds(geometry)) \
  .map(maskS2clouds) 

def addNDVI(image):
  ndvi = image.normalizedDifference(['B5', 'B4']).rename('ndvi')
  return image.addBands(ndvi)

withNdvi = filtered.map(addNDVI)
medita = withNdvi.median()

image_ids = withNdvi.aggregate_array('system:index').getInfo()
print('Total images: ', len(image_ids))

for i, image_id in enumerate(image_ids):
  image = ee.Image(withNdvi.filter(ee.Filter.eq('system:index', image_id)).first())
  task = ee.batch.Export.image.toDrive(**{
      'image': image.select('ndvi'),
      'description': 'Image Export {}'.format(i+1),
      'fileNamePrefix': image.id().getInfo(),
      'folder': 'Example_folder',
      'scale': 100,
      'region': image.geometry().bounds().getInfo()['coordinates'],
      'maxPixels': 1e10
  })
  task.start()
  print('Started Task: ', i+1)