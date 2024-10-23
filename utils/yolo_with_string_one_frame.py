# without while loop means single image capture and string bhi de dega
import cv2
import torch
import numpy as np
import os
import pytesseract
from utils.db

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
path1 = '/usr/local/lib/python3.9/dist-packages/yolov5/best.pt'

model = torch.hub.load('ultralytics/yolov5', 'custom', path1, force_reload=True)
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame = cv2.resize(frame, (1020, 500))
results = model(frame)

bboxes = results.xyxy[0].cpu().numpy() # extract bounding boxes
for box in bboxes:
    x1, y1, x2, y2 = box[:4].astype(int)
    cropped_img = frame[y1:y2, x1:x2] # crop image to bounding box
    text = pytesseract.image_to_string(cropped_img, config='--psm 11')
    text = text.replace('\n', '').replace('\x0c', '') # clean up text
    print(text)
    cv2.putText(frame, text, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # draw text on frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) # draw bounding box on frame

cv2.imshow("FRAME", frame)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
