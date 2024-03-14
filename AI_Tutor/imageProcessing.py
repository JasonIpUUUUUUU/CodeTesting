import os
import cv2 as cv

folder_path = "Images"
output_folder = "path"

images = os.listdir(folder_path)

image_files = [file for file in images]

img = cv.imread(image_files[0])

cv.imshow("original image", img)
cv.waitKey(0)