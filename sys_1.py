
from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter import PhotoImage
import subprocess
import cv2
import smtplib
from email.message import EmailMessage
import os

class StudentManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Management System")
        self.window.geometry("400x250")

        self.logo_image = PhotoImage(file="logo.png")

        # Label
        self.logo_label = Label(window, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.id_label = Label(window, text="ID:", font=("Arial", 16))
        self.id_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

        self.pass_label = Label(window, text="Password:", font=("Arial", 16))
        self.pass_label.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        self.id_entry = Entry(window, font=("Arial", 16))
        self.id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

        self.pass_entry = Entry(window, show="*", font=("Arial", 16))
        self.pass_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")

        self.login_btn = Button(window, text="Login", font=("Arial", 16), command=self.login)
        self.login_btn.grid(row=2, column=2, padx=10, pady=10, sticky="W")

        # Storage file
        self.storage_file = "storage.txt"
        self.clear_storage_file()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) # window close event

    def login(self):
        student_file = "names.txt"  # File containing student names, ID, and passwords
        student_data = self.read_student_data(student_file)

        student_id = self.id_entry.get()
        password = self.pass_entry.get()  # transform password as string

        if student_id == "1121122" and student_id in student_data and student_data[student_id]["password"] == password:
            messagebox.showinfo("Login", "Login successful!")

            # Store ID and password in the storage file
            self.store_credentials(student_id, password)

            stored_id, stored_password = self.get_stored_credentials()

            self.run_main()
            self.open_monitor()

            self.window.destroy()  # Close the window on successful login
        elif student_id in student_data and student_data[student_id]["password"] == password:
            messagebox.showinfo("Login", "Login successful!")

            # Store ID and password in the storage file
            self.store_credentials(student_id, password)

            stored_id, stored_password = self.get_stored_credentials()

            self.run_main()
            self.open_monitor()

            if student_id != "1121122":
                self.store_face_recognition_result(student_data[stored_id]["name"])

            self.window.after(2000, self.send_cheat_email, student_data[stored_id]["name"])

            self.window.after(4000, self.window.destroy)  # Close the window after 4 seconds
        else:
            messagebox.showerror("Login", "Wrong ID or password. Please try again.")

    def on_closing(self):
        self.clear_storage_file()
        self.window.destroy()

    def clear_storage_file(self):
        # Clear the storage file
        with open(self.storage_file, "w") as f:
            f.write("")

    def store_credentials(self, student_id, password):
        # Append ID and password to the storage file
        with open(self.storage_file, "a") as f:
            f.write(f"{student_id},{password}\n")

    def get_stored_credentials(self):
        # Read the stored ID and password from the storage file
        with open(self.storage_file, "r") as f:
            line = f.readline().strip()
            stored_id, stored_password = line.split(",") if line else ("", "")
        return stored_id, stored_password

    def read_student_data(self, file):
        student_data = {}
        with open(file, "r") as f:
            for line in f:
                name, student_id, password = line.strip().split(",")
                student_data[student_id] = {
                    "name": name,
                    "password": password
                }
        return student_data

    def open_monitor(self):
        # Open the monitor code goes here
        # Modify this method with the appropriate code to open the monitor
        subprocess.Popen(['python', 'monitor.py'])

    def run_main(self):
        # Run the main.py script
        subprocess.Popen(['python', 'main.py'])

    def store_face_recognition_result(self, student_name):
        # Store the face recognition result in the storage file
        with open(self.storage_file, "a") as f:
            f.write(f"Face recognition result: {student_name}\n")

    def send_cheat_email(self, student_name):
        # Example email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'haydariifatimaa@gmail.com'
        sender_password = 'nnjgtxozppavhkzz'
        recipient_email = 'fza122@usal.edu.lb'
        subject = 'Cheating Alert'
        message = f'{student_name} is suspected of cheating.'

        try:
            # Create and configure the email message
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg.set_content(message)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print('Email sent successfully!')
        except Exception as e:
            print('An error occurred while sending the email:', str(e))


window = Tk()
app = StudentManagementGUI(window)
window.mainloop()
