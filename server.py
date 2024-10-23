import flask
import pymongo
import datetime
import json
# from utils import number_plate
from flask import Flask,render_template, request, redirect, url_for, session, make_response, jsonify, send_file
import hashlib
import json
import csv
from io import StringIO, BytesIO
from flask_pymongo import PyMongo
import codecs
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
        text = "".join(text[:].split(" "))
        if(len(text)>9):
            text = text[:-1]
        # text = "HR72B8058"
        return text



def date_from_timestamp(timestamp):
    if timestamp is None:
        return ""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')

def time_from_timestamp(timestamp):
    if timestamp is None:
        return ""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%I:%M:%S %p')

app = Flask(__name__)
app.config["DEBUG"]=True

# connecting with database
app.config["MONGO_URI"] = "mongodb://localhost:27017/bmu_aves"
app.secret_key = "v3a"
mongo = PyMongo(app)
credentials = mongo.db.login_credentials
vehicle_log = mongo.db.vehicle_log

app.app_context().push()

@app.route("/")
def send_login_page():
    session['login_status'] = False
    msg="Welcome!"
    return render_template("./login.html",msg=msg)

@app.route("/login",methods=['POST','GET'])
def verifyLogin():
    username = request.form.get("username")
    password = request.form.get("password")
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password == credentials.find_one({"username":username})["password"]:
        msg = 'Logged in successfully!'
        session['login_status'] = True
        return make_response(msg)
    else:
        msg = 'Incorrect username / password!'
        response = make_response(msg)
        response.status_code = 401
        return response

@app.route("/dashboard",methods=["GET"])
def render_dashboard():
    if session.get('login_status'):
        return render_template("./bmu.html")
    else:
        return render_template("./login.html")

@app.route("/auto_in_fill",methods=["GET"])
def auto_in_fill():
    img = in_camera_img()
    vehicle_no = get_string_from_img(img)
    # vehicle_no = vehicle_no[:-1]
    # vehicle_no = "Ava114CH3"
    driver_name = ""
    mobile_number = ""
    visit_category = ""
    log_data = vehicle_log.find_one({"vehicle_no":vehicle_no})
    if log_data is not None:
        driver_name = log_data["driver_name"]
        mobile_number = log_data["mobile_number"]
        visit_category = log_data["visit_category"]
    response = {"driver_name":driver_name,
              "vehicle_no":vehicle_no,
              "mobile_number":mobile_number,
              "visit_category":visit_category}
    return jsonify(response)

@app.route("/auto_out_fill",methods=["GET"])
def auto_out_fill():
    img = out_camera_img()
    vehicle_no = get_string_from_img(img)
    # vehicle_no = "Ava114CH3"
    driver_name = ""
    mobile_number = ""
    visit_category = ""
    log_data = vehicle_log.find_one({"vehicle_no":vehicle_no})
    print(log_data)
    if log_data is not None:
        driver_name = log_data["driver_name"]
        mobile_number = log_data["mobile_number"]
        visit_category = log_data["visit_category"]
    response = {"driver_name":driver_name,
              "vehicle_no":vehicle_no,
              "mobile_number":mobile_number,
              "visit_category":visit_category,}
    return jsonify(response)

@app.route("/submit_in_data",methods=["PUT"])
def submit_in_data():
    global vehicle_log, request
    data = request.get_json()
    vehicle_no = data["vehicle_no"]
    driver_name = data["driver_name"]
    mobile_number = data["mobile_number"]
    visit_category = data["visit_category"]
    in_time = datetime.datetime.now().timestamp()
    response = {"driver_name":driver_name,
              "vehicle_no":vehicle_no,
              "in_time":in_time,
              "out_time":None,
              "mobile_number":mobile_number,
              "visit_category":visit_category}
    vehicle_log.insert_one(response)
    return jsonify({"message": "Data inserted successfully."})

@app.route("/submit_out_data", methods=["PUT"])
def submit_out_data():
    global vehicle_log, request
    data = request.get_json()
    print(data)
    vehicle_no = data["vehicle_no"]
    driver_name = data["driver_name"]
    mobile_number = data["mobile_number"]
    visit_category = data["visit_category"]
    out_time = datetime.datetime.now().timestamp()
    # Update the document for the visitor with the given vehicle number
    res = vehicle_log.update_one(
        {"_id": vehicle_log.find_one({"vehicle_no":vehicle_no},sort=[('_id', -1)])["_id"]},
        {"$set": {"driver_name":driver_name,"mobile_number":mobile_number,"out_time": out_time, "visit_category":visit_category}}
    )
    if res.acknowledged:
        return jsonify({"message": "Data updated successfully."})
    else:
        return jsonify({"message":"Data not updated."})

@app.route("/download_daily_csv", methods=["GET"])
def download_daily_csv():
    # Get the vehicle logs for the last 1 day
    today = datetime.datetime.now().timestamp()
    yesterday = today - 86400 # 86400 seconds = 1 day
    daily_logs = vehicle_log.find({"in_date": {"$gte": yesterday}})
    
    # Create a CSV file
    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(["Driver Name", "Vehicle No.", "Mobile Number", "Visit Category", "In Time", "Out Time", "In Date", "Out Date"])
    for log in daily_logs:
        in_time = log["in_time"]
        out_time = log["out_time"]
        writer.writerow([log["driver_name"], log["vehicle_no"], log["mobile_number"], log["visit_category"], time_from_timestamp(in_time), time_from_timestamp(out_time), date_from_timestamp(in_time), date_from_timestamp(out_time)])
    file.seek(0)
    csv_bytes = file.getvalue().encode("utf-8")
    # Send the CSV file as a response
    response = make_response(BytesIO(csv_bytes))
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='daily_vehicle_logs.csv')
    return response

@app.route("/download_weekly_csv", methods=["GET"])
def download_weekly_csv():
    # Get the vehicle logs for the last 7 days
    today = datetime.datetime.now().timestamp()
    week_ago = today - 604800 # 604800 seconds = 7 days
    weekly_logs = vehicle_log.find({"in_date": {"$gte": week_ago}})
    
    # Create a CSV file 
    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(["Driver Name", "Vehicle No.", "Mobile Number", "Visit Category", "In Time", "Out Time", "In Date", "Out Date"])
    for log in weekly_logs:
        in_time = log["in_time"]
        out_time = log["out_time"]
        writer.writerow([log["driver_name"], log["vehicle_no"], log["mobile_number"], log["visit_category"], time_from_timestamp(in_time), time_from_timestamp(out_time), date_from_timestamp(in_time), date_from_timestamp(out_time)])
    file.seek(0)
    csv_bytes = file.getvalue().encode("utf-8")
    # Send the CSV file as a response
    response = make_response(BytesIO(csv_bytes))
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='weekly_vehicle_logs.csv')
    return response

@app.route("/download_monthly_csv",methods=["GET"])
def download_monthly_csv():
    # Get the vehicle logs for the last 30 days
    today = datetime.datetime.now().timestamp()
    month_ago = today - 2592000 # 2592000 seconds = 30 days
    monthly_logs = vehicle_log.find({"in_date": {"$gte": month_ago}})
    
    # Create a CSV file
    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(["Driver Name", "Vehicle No.", "Mobile Number", "Visit Category", "In Time", "Out Time", "In Date", "Out Date"])
    for log in monthly_logs:
        in_time = log["in_time"]
        out_time = log["out_time"]
        writer.writerow([log["driver_name"], log["vehicle_no"], log["mobile_number"], log["visit_category"], time_from_timestamp(in_time), time_from_timestamp(out_time), date_from_timestamp(in_time), date_from_timestamp(out_time)])
    file.seek(0)
    csv_bytes = file.getvalue().encode("utf-8")
    # Send the CSV file as a response
    response = make_response(BytesIO(csv_bytes))
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='monthly_vehicle_logs.csv')
    return response




if __name__=="__main__":
    app.run()