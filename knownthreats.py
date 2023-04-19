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

# Add these imports
import os
import pickle
from imutils.video import VideoStream

# Configuration
email = "your_email@gmail.com"  # Replace with your email
password = "your_password"  # Replace with your email password
receiver_email = "alexis01valentino@gmail.com"
haar_cascade_path = "path/to/haar_cascade.xml"  # Replace with the path to your haar cascade file
known_faces_model_path = "path/to/known_faces.pickle"  # Replace with the path to your known faces model

# Load known faces model
with open(known_faces_model_path, 'rb') as f:
    known_faces = pickle.load(f)

# Initialize DNN face detector and recognizer
protoPath = "path/to/deploy.prototxt"
modelPath = "path/to/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
embedder = cv2.dnn.readNetFromTorch("path/to/openface_nn4.small2.v1.t7")

# ... (rest of the code remains the same)

# Main loop
while True:
    ret, frame = camera.read()

    # ... (previous code remains the same)

    # Face detection
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    unknown_faces = []

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        (fH, fW) = face.shape[:2]

        # Create a blob from the face region
        face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        embedder.setInput(face_blob)
        vec = embedder.forward()

        # Find the known face with the smallest distance to the new face
        min_distance = 1000
        known_face_name = None
        for name, embeddings in known_faces.items():
            for embedding in embeddings:
                distance = np.linalg.norm(embedding - vec)
                if distance < min_distance:
                    min_distance = distance
                    known_face_name = name

        # Check if the face is a known face
        if min_distance < 0.5:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, known_face_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        else:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            unknown_faces.append((x, y, w, h))

    # ... (rest of the code remains the same)

    # Replace 'if face_detected:' with 'if' rest of the code remains the same)

    # Trigger alarms and send email notifications for known faces
    if known_face_name:
        if not face_alarm_active:
            play_alarm_for(10)
            face_alarm_active = True
            screenshot = "face_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Known Face Detected", f"A known face ({known_face_name}) has been detected.", screenshot, "detection.jpg", MIMEImage)
    else:
        face_alarm_active = False

    # Trigger alarms and send email notifications for unknown faces
    if unknown_faces:
        if not face_alarm_active:
            play_alarm_for(10)
            face_alarm_active = True
            screenshot = "unknown_face_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Unknown Face Detected", "An unknown face has been detected.", screenshot, "detection.jpg", MIMEImage)
    else:
        face_alarm_active = False

    # ... (rest of the code remains the same)

camera.release()
cv2.destroyAllWindows()
pygame.quit()

