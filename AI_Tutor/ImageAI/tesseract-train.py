import os
import subprocess
import cv2
from imageProcessing import preprocess

def train_ocr(image_path, text_path, model_name):
    images = os.listdir(image_path)
    image_files = [os.path.join(image_path, file) for file in images]

    texts = os.listdir(text_path)
    text_files = [os.path.join(text_path, file) for file in texts]

    for (image_file, text_file) in (zip(image_files, text_files)):
        img = cv2.imread(image_file)
        processed_image = preprocess(img)
        
        create_box_command = f"tesseract {processed_image} {text_file} nobatch box.train"
        subprocess.run(create_box_command, shell=True)
        
        unicharset_command = f"unicharset_extractor {text_file}"
        subprocess.run(unicharset_command, shell=True)
        
        mftraining_command = f"mftraining -F font_properties -U {text_path}/unicharset -O {model_name} {text_path}/proto.tr"
        subprocess.run(mftraining_command, shell=True)
        
        cntraining_command = f"cntraining {text_path}/proto.tr"
        subprocess.run(cntraining_command, shell=True)
        
        combine_command = f"combine_tessdata {model_name}"
        subprocess.run(combine_command, shell=True)

if __name__ == "__main__":
    image_path = "math-ground-truth"
    text_path = "math-text"
    model_name = "mathModel"
    train_ocr(image_path, text_path, model_name)