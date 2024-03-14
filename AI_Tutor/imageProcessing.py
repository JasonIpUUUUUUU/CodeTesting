import os
import cv2 as cv

folder_path = "Images"
output_folder = "path"

images = os.listdir(folder_path)

image_files = [os.path.join(folder_path, file) for file in images]

img = cv.imread(image_files[0])

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow("Grayscale image", gray_img)
cv.waitKey(0)