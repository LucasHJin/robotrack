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

# Process existing frames
input_dir = "data"
output_dir = "filtered_data"
os.makedirs(output_dir, exist_ok=True)

text_region = (830, 15, 260, 45)  # adjusted parameters based on video
frame = cv2.imread(os.path.join(input_dir, "frame_00012.jpg"))
print(get_text(frame, text_region))

"""
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".jpg"):
        frame = cv2.imread(os.path.join(input_dir, filename))
        if has_numbers_in_region(frame, text_region):
            cv2.imwrite(os.path.join(output_dir, filename), frame)
            print(f"Kept: {filename}")
        else:
            print(f"Skipped: {filename}")"""