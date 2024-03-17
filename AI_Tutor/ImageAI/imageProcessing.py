import os
import cv2
import pytesseract
import numpy as np

def noise_removal(image):
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8) #redefined in case for special cases
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 1)
    return (image)

#https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def detectStructures(image):
    # processing the image so the structures can be more easily identified
    newImage = image.copy()
    blurredImage = cv2.GaussianBlur(newImage, (7,7), 0)
    thresh = cv2.threshold(blurredImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16, 10))
    blurredImage = cv2.dilate(thresh, kernel, iterations=1)
    cnts = cv2.findContours(blurredImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        roi = newImage[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
        if text:
            with open("results.txt", "a") as f:
                f.write(text.replace('\n', ' ').strip() + '\n')
        cv2.rectangle(newImage, (x, y), (x + w, y + h), (36, 255, 12), 2)
    return newImage

def preprocess(img):
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, processed_img = cv2.threshold(processed_img, 190, 255, cv2.THRESH_BINARY)
    processed_img = noise_removal(processed_img)
    return processed_img

folder_path = "Images"

images = os.listdir(folder_path)

image_files = [os.path.join(folder_path, file) for file in images]

img = cv2.imread(image_files[2])

processed_img = preprocess(img)

processed_img = detectStructures(processed_img)

cv2.imshow("processed image", processed_img)
cv2.waitKey(0)

result = pytesseract.image_to_string(processed_img)
