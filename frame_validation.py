import pytesseract
from PIL import Image
import cv2
import os

def get_text(frame, region):
    x, y, w, h = region
    roi = frame[y:y+h, x:x+w]
    roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(roi_pil).strip()
    return text

def validate_frame(input_dir, output_dir):
    TEXT_REGION = (830, 15, 260, 45) 
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".jpg"):
            frame = cv2.imread(os.path.join(input_dir, filename))
            text = get_text(frame, TEXT_REGION)
            if "qualification" in text.lower():
                cv2.imwrite(os.path.join(output_dir, filename), frame) # type: ignore
            os.remove(os.path.join(input_dir, filename))  
            
            
validate_frame("data/raw", "data/clean")
