import os
import cv2 as cv

folder_path = "Images"
output_folder = "path"

if os.path.exists(folder_path):
    print("image folder found")
else:
    print("image folder not found")

images = os.listdir(folder_path)

image_files = [file for file in images]