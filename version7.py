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

# Configuration
email = "your_email@gmail.com"  # Replace with your email
password = "your_password"  # Replace with your email password
receiver_email = "alexis01valentino@gmail.com"
haar_cascade_path = "path/to/haar_cascade.xml"  # Replace with the path to your haar cascade file

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

# Main loop
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
    face_detected = len(faces) > 0

    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Audio detection
    audio_data = audio_detection()
    unusual_sound_detected = False  # Replace with your audio detection logic

   
    # Trigger alarms and send email notifications
    if gun_detected:
        if not gun_alarm_active:
            play_alarm_for(10)
            gun_alarm_active = True
            screenshot = "gun_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Gun Detected", "A gun has been detected.", screenshot, "detection.jpg", MIMEImage)
    else:
        gun_alarm_active = False

    if unusual_sound_detected:
        if not sound_alarm_active:
            play_alarm_for(10)
            sound_alarm_active = True
            audio_file = "unusual_sound.wav"
            write(audio_file, 44100, audio_data)
            send_email("Unusual Sound Detected", "An unusual sound has been detected.", audio_file, "unusual_sound.wav", MIMEAudio)
    else:
        sound_alarm_active = False

    if face_detected:
        if not face_alarm_active:
            play_alarm_for(10)
            face_alarm_active = True
            screenshot = "face_screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email("Known Face Detected", "A known face has been detected.", screenshot, "detection.jpg", MIMEImage)
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
