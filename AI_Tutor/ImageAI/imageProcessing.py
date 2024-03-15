import os
import cv2
import pytesseract

folder_path = "Images"
output_folder = "path"

images = os.listdir(folder_path)

image_files = [os.path.join(folder_path, file) for file in images]

img = cv2.imread(image_files[0])

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

result = pytesseract.image_to_string(gray_img)

output_file_path = os.path.join("results.txt")
with open(output_file_path, 'w') as f:
    f.write(result)
