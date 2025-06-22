

# 🔥 Face Recognition & Fire Detection System

A smart and interactive Python-based security system that detects unauthorized faces and fire events, and notifies responsible parties in real-time via email and visual alerts.

---

## 🎯 Objective
The aim of this project is to detect unauthorized individuals and fire, and send email alerts to the relevant authority.

---

## 🧠 Features
- Face recognition using webcam in real time
- Sends email if face is not recognized (includes ID and name)
- Fire detection using OpenCV and color thresholding
- Email alert for fire with room identification
- Login system for students with validation and cheating detection
- Integrated audio alert and GUI (Tkinter)
- Separate actions for authorized and unauthorized logins
- GUI clears stored data on close

---

## 💻 Technologies & Libraries
- `cv2` (OpenCV)
- `face_recognition`
- `numpy`
- `tkinter`
- `smtplib`, `email.mime`
- `subprocess`, `os`
- `pygame`
- `PIL`

---

## 📁 Project Structure
face-recognition-fire-detection/
├── main.py
├── sys_1.py
├── photos/
├── fire_detection.xml
├── storage.txt
├── names.txt
├── id.txt
├── audio.mp3
├── README.md



---

## ⚠️ Problems & Solutions

**🔥 fire_detection.xml missing?**  
Make sure it's in the correct folder and valid.

**🔐 Email security:**  
Move credentials to environment variables or a config file to stay secure.

---

## 🚀 How to Run
```bash
pip install -r requirements.txt
python login.py

