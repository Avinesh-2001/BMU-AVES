import numpy as np
import cv2
import pytesseract
import torch

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

cam1_ip = "ip_addr_cam_1"
cam2_ip = "ip_addr_cam_2"

path_to_model_weights = "C:/Users/vasud/.cache/torch\hub/ultralytics_yolov5_master/best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path_to_model_weights, force_reload=False)

# cam1 = cv2.VideoCapture(cam1_ip)
# cam2 = cv2.VideoCapture(cam2_ip)

def in_camera_img():
    # ret, frame = cam1.read()
    frame = cv2.imread("D:/BMU/Semester6/MajorProject/BMU-AVES/utils/wagnor.jpeg")
    return frame

def out_camera_img():
    # ret, frame = cam2.read()
    frame = cv2.imread("D:/BMU/Semester6/MajorProject/BMU-AVES/utils/wagnor.jpeg")
    return frame
    
def get_string_from_img(img)->str:
    img = cv2.resize(img, (1020, 500))
    results = model(img)

    bboxes = results.xyxy[0].cpu().numpy() # extract bounding boxes
    for box in bboxes:
        x1, y1, x2, y2 = box[:4].astype(int)
        cropped_img = img[y1:y2, x1:x2] # crop image to bounding box
        text = pytesseract.image_to_string(cropped_img, config='--psm 11')
        text = text.replace('\n', '').replace('\x0c', '')
        text = "".join(text[:-1].split(" "))
        return text
    
if __name__=="__main__":
    img = cv2.imread("D:/BMU/Semester6/MajorProject/BMU-AVES/utils/wagnor.jpeg")
    
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    text = get_string_from_img(img)
    print("".join(text[:-1].split(" ")))