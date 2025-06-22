
import cv2
import numpy as np
import face_recognition
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import Tk, Label, Button
from PIL import ImageTk, Image
import pygame

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

cap = cv2.VideoCapture(0)

path = 'photos'
images = []
classNames = []
personsList = os.listdir(path)

for cl in personsList:
    curPersonn = cv2.imread(f'{path}/{cl}')
    images.append(curPersonn)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Load ID and password from names.txt
id_password_map = {}
with open('names.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            name, id, password = line.split(',')
            id_password_map[name.lower()] = (id, password)

def findEncodeings(image):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodeings(images)
print('Encoding Complete.')

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def send_email(sender_email, receiver_email, subject, message, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print('Email sent successfully')
        server.quit()
    except Exception as e:
        print('Error sending email:', str(e))
        
def store_detected_name(name):
    with open("storage.txt", "r+") as file:
        lines = file.readlines()
        lowercase_name = name.lower()  # Convert the name to lowercase

        # Check if name already exists in storage.txt
        name_exists = False
        for i, line in enumerate(lines):
            if line.startswith(lowercase_name):
                name_exists = True
                break
        
        if not name_exists:
            lines.append(f"{lowercase_name}\n")
        
        # Clear the file and write the updated lines
        file.seek(0)
        file.truncate()
        file.writelines(lines)

# Email account details
sender_email = ''
sender_password = ''
receiver_email = ''
fire_subject = 'Fire in the room'
fire_message = 'There is a fire in the room!'

class DoctorInterface:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.label = Label(root, text="Monitoring System", font=('Arial', 18), fg='white', bg='black')
        self.label.pack(side='bottom', pady=50)
        self.button = Button(root, text="Start Monitoring", font=('Arial', 16), bg='white', fg='black', command=self.start_monitoring)
        self.button.pack(side='bottom', pady=20)
        self.email_sent = False
        self.fire_detected = False

    def start_monitoring(self):
        self.button.config(state="disabled")
        self.label.config(text="Monitoring in progress...", font=('Arial', 16), fg='white')

        self.monitoring_loop(sender_email, receiver_email, sender_password, fire_subject, fire_message)

    def monitoring_loop(self, sender_email, receiver_email, sender_password, fire_subject, fire_message):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

        if len(fire) > 0:
            play_audio('audio.mp3')
            if not self.fire_detected:
                self.fire_detected = True
                send_email(sender_email, receiver_email, fire_subject, fire_message, sender_password)
                self.label.config(text="Please leave the room if you can", font=('Arial', 16), fg='white')

        faceCurrentFrame = face_recognition.face_locations(imgS)
        encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

        for encodeface, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                store_detected_name(name)  # Write the name to storage.txt

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                if self.fire_detected and not self.email_sent:
                    self.email_sent = True
                    send_email(sender_email, receiver_email, fire_subject, f"{fire_message} Detected Person: {name}", sender_password)

        cv2.imshow('Monitoring', frame)
        if cv2.waitKey(1) & 0xFF == 13:
            self.stop_monitoring()

        self.root.after(1, self.monitoring_loop, sender_email, receiver_email, sender_password, fire_subject, fire_message)

    def stop_monitoring(self):
        self.label.config(text="Monitoring stopped.", font=('Arial', 16), fg='white')
        self.button.config(state="normal")

root = Tk()
root.title("Doctor Interface")
root.geometry("800x600")

# Set the background image
background_image = ImageTk.PhotoImage(Image.open("back.jpg"))
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

interface = DoctorInterface(root)
root.mainloop()


