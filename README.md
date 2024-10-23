BMU Automated Vehicle Entry System (BMU AVES) 🚗🔒


🌟 Overview
BMU AVES (Automated Vehicle Entry System) is a smart solution designed to automate vehicle entry and exit at BMU's Gate-2. This project leverages License Plate Recognition (LPR) technology and Optical Character Recognition (OCR) to detect and recognize vehicle number plates, allowing authorized vehicles to pass through automatically, without manual intervention.

By utilizing YOLOv5 for vehicle detection and Pytesseract for text extraction, BMU AVES ensures high accuracy and real-time processing, running seamlessly on a Raspberry Pi to manage entry/exit in a cost-effective manner.

⚙️ Key Features

📸 License Plate Recognition (LPR): Real-time detection and recognition of vehicle license plates.
🔍 Optical Character Recognition (OCR): Extracts vehicle number details using Pytesseract.
💻 Web-based GUI: Intuitive interface for monitoring entries, managing vehicle data, and viewing owner details.
🔗 Raspberry Pi Integration: Portable, low-cost real-time processing on Raspberry Pi.
⚡ Enhanced Accuracy: Optimized vehicle detection with YOLOv5 for superior performance.
🗃️ Automated Data Logging: Logs vehicle entries and exits into the system database automatically.
🌍 Environmentally Friendly: Reduces paper usage by digitizing the vehicle entry process.
💡 Cost-effective: Completed within a budget of ₹40-50k, significantly lower than the market estimate of ₹1-2 lakhs.

🛠️ Project Architecture

- Frontend: Built using HTML, CSS, and JavaScript for a smooth, responsive web interface.
- Backend: Powered by Python with Flask for API handling and database management.
- AI Models: Uses YOLOv5 for vehicle detection and Pytesseract for OCR to extract text from number plates.
- Raspberry Pi: Handles real-time image processing and vehicle entry data logging.


💻 Technologies Used

Python 🐍
Flask (Backend API)
YOLOv5 (Vehicle Detection)
Pytesseract (OCR)
OpenCV (Image Processing)
MySQL (Database)
HTML/CSS/JavaScript (Frontend for GUI)
Raspberry Pi (Hardware)

🚀 Set Up

1. Clone the Repository:

git clone https://github.com/Avinesh-2001/BMU-Automated-Vehicle-Entry-System.git
cd BMU-Automated-Vehicle-Entry-System

2. Install Dependencies:

pip install -r requirements.txt

3. Run the Backend:
cd app/backend
python app.py
