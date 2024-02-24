#The code below has been run on Jupyter notebook, it's purpose is to download images from SentinelHub and process the image via cropping it and joining it back together

from sentinelhub import BBox, CRS, DataCollection, MimeType, MosaickingOrder, bbox_to_dimensions
from sentinelhub import SentinelHubRequest, SHConfig
import matplotlib.pyplot as plt
import os
from PIL import Image

cropped_images = []

def join_cropped_images(cropped_images, rows, columns, output_path='joined_image.jpeg'):
    images = [Image.open(image_path) for image_path in cropped_images]

    image_width, image_height = images[0].size

    joined_width = columns * image_width
    joined_height = rows * image_height

    joined_image = Image.new('RGB', (joined_width, joined_height))
    
    imgIndex = 0
    
    for i in range(rows):
        for j in range(columns):
            start_x = j * image_width
            start_y = i * image_height
            joined_image.paste(images[imgIndex], (start_x, start_y))
            imgIndex += 1

    joined_image.save(output_path)
    joined_image.show()

def plot_image(image, willShow = False, factor=1 / 255, clip_range=(0, 1), crop_size=None, display_all_crops=False):
    image = image * factor
    image[image < clip_range[0]] = clip_range[0]
    image[image > clip_range[1]] = clip_range[1]

    if display_all_crops and crop_size:
        height, width, _ = image.shape
        crop_rows, crop_cols = crop_size
        num_rows = height // crop_rows
        num_cols = width // crop_cols

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 20, num_rows * 20))

        for i in range(num_rows):
            for j in range(num_cols):
                start_row, end_row = i * crop_rows, (i + 1) * crop_rows
                start_col, end_col = j * crop_cols, (j + 1) * crop_cols

                cropped_image = Image.fromarray((image[start_row:end_row, start_col:end_col, :] * 255).astype('uint8'))
                axs[i, j].imshow(cropped_image)
                axs[i, j].axis('off')
                
                cropped_image_path = f'cropped_image_{i}_{j}.jpeg'
                cropped_image.save(cropped_image_path)
                cropped_images.append(cropped_image_path)
                if willShow:
                    cropped_image.show()

        plt.show()

    else:
        plt.imshow(image)
        plt.show()
    return num_rows, num_cols

betsiboka_coords_wgs84 = (45.16, -17.15, 46.51, -15.58)
resolution = 100
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")
evalscript_all_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12"],
                units: "DN"
            }],
            output: {
                bands: 13,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01,
                sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B09,
                sample.B10,
                sample.B11,
                sample.B12];
    }
"""

request_all_bands = SentinelHubRequest(
    evalscript=evalscript_all_bands,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=("2020-06-01", "2020-06-30"),
            mosaicking_order=MosaickingOrder.LEAST_CC,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

all_bands_response = request_all_bands.get_data()

rows, cols = plot_image(all_bands_response[0][:, :, [3, 2, 1]], willShow = True, factor=3.5 / 1e4, crop_size=(500, 500), display_all_crops=True)

join_cropped_images(cropped_images, rows = rows, columns = cols, output_path='joined_image.png')