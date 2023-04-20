import numpy as np
import cv2
import imutils
import datetime
import pygame
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import sounddevice as sd
from scipy.io.wavfile import write
import io
import os
import pickle
from imutils.video import VideoStream

# Configuration
email = ""  # Replace with your email
password = ""  # Replace with your email password or app generated password
receiver_email = "" # Replace with the recipients email
haar_cascade_path = "C:/Users/ACER/Desktop/Real time threat detection/face_cascade.xml"  # Replace with the path to your haar cascade file
known_faces_model_path = "C:/Users/ACER/Desktop/Real time threat detection/models/known_faces.pkl"  # Replace with the path to your known faces model
homeowner_faces_model_path = "C:/Users/ACER/Desktop/Real time threat detection/models/home_owners.pkl"  # Replace with the path to your homeowner faces model

# Load known faces and homeowner faces models
with open(known_faces_model_path, 'rb') as f:
    known_faces = pickle.load(f)

with open(homeowner_faces_model_path, 'rb') as f:
    homeowner_faces = pickle.load(f)

# Initialize DNN face detector and recognizer
protoPath = "C:/Users/ACER/Desktop/Real time threat detection/models/deploy.prototxt"
modelPath = "C:/Users/ACER/Desktop/Real time threat detection/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
embedder = cv2.dnn.readNetFromTorch("C:/Users/ACER/Desktop/Real time threat detection/models/openface_nn4.small2.v1.t7")

# Initialize
gun_cascade = cv2.CascadeClassifier('cascade.xml')
face_cascade = cv2.CascadeClassifier(haar_cascade_path)
camera = cv2.VideoCapture(0)

pygame.init()
alarm_sound = pygame.mixer.Sound('alarm.wav')

gun_alarm_active = False
sound_alarm_active = False
face_alarm_active = False

# Audio detection function
def audio_detection():
    fs = 44100
    duration = 2  # seconds
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    return audio_data

def play_alarm_for(seconds):
    alarm_sound.play(-1)
    pygame.time.delay(seconds * 1000)
    alarm_sound.stop()

# Email sending function
def send_email(subject, body, attachment=None, attachment_name=None, attachment_mime=None):
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    if attachment is not None:
        with open(attachment, 'rb') as f:
            attachment_data = f.read()
        attachment_mime = attachment_mime(attachment_data, name=attachment_name)
        message.attach(attachment_mime)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, receiver_email, message.as_string())

def find_closest_face(vec, faces_list):
    min_distance = 1000
    closest_face = None
    for name, embeddings in faces_list.items():
        for embedding in embeddings:
            distance = np.linalg.norm(embedding - vec)
            if distance < min_distance:
                min_distance = distance
                closest_face = name
    return closest_face, min_distance

while True:
    ret, frame = camera.read()

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gun detection
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))
    gun_detected = len(gun) > 0

    for (x, y, w, h) in gun:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Face detection
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_detected = False
    homeowner_face_detected = False

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        (fH, fW) = face.shape[:2]

        # Create a blob from the face region
        face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        embedder.setInput(face_blob)
        vec = embedder.forward()

        # Find the closest matching face in known_faces and homeowner_faces
        closest_known_face, known_face_distance = find_closest_face(vec, known_faces)
        closest_homeowner_face, homeowner_face_distance = find_closest_face(vec, homeowner_faces)

        # Check if the face is a known face or a homeowner face
        if known_face_distance < 0.5:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, closest_known_face, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            face_detected = True
        elif homeowner_face_distance < 0.5:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, closest_homeowner_face, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            homeowner_face_detected = True
        else:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Audio detection
    audio_data = audio_detection()
    unusual_sound_detected = False  # Replace with your audio detection logic

    # Trigger alarms and send email notifications
    if gun_detected:
        if not gun_alarm_active:
            play_alarm_for(15)
            gun_alarm_active = True
            screenshot = "gun_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Gun Detected", "A gun has been detected.", screenshot, "detection.jpg", MIMEImage)
    else:
        gun_alarm_active = False

    if unusual_sound_detected:
        if not sound_alarm_active:
            play_alarm_for(15)
            sound_alarm_active = True
            audio_file = "unusual_sound.wav"
            write(audio_file, 44100, audio_data)
            send_email("Unusual Sound Detected", "An unusual sound has been detected.", audio_file, "unusual_sound.wav", MIMEAudio)
    else:
        sound_alarm_active = False

    if face_detected:
        if not face_alarm_active:
            play_alarm_for(15)
            face_alarm_active = True
            screenshot = "face_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Known Face Detected", f"A known face ({closest_known_face}) has been detected.", screenshot, "detection.jpg", MIMEImage)
    else:
        face_alarm_active = False

    if homeowner_face_detected:
        # No alarm for homeowner faces
        pass
    else:
        if not face_alarm_active:
            play_alarm_for(15)
            face_alarm_active = True
            screenshot = "unknown_face_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Unknown Face Detected", "An unknown face has been detected.", screenshot, "detection.jpg", MIMEImage)
        else:
            face_alarm_active = False

    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
pygame.quit()
