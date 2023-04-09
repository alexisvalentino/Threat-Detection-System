import numpy as np
import cv2
import imutils
import smtplib
import datetime
import pygame
import sounddevice as sd
import soundfile as sf
import os
import tensorflow as tf

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# Set the email address and password for the email account that will be used to send notifications
EMAIL_ADDRESS = 'sendo2127@gmail.com'
EMAIL_PASSWORD = 'arenaofvalor#0@16'

# Set the directory where the known faces are stored
KNOWN_FACES_DIR = 'known_faces'

# Set the sound threshold for detecting unusual sounds
SOUND_THRESHOLD = 0.001

# Load the cascade classifier for detecting guns
gun_cascade = cv2.CascadeClassifier('cascade.xml')

# Start the camera
camera = cv2.VideoCapture(0)

# Initialize variables for detecting guns and activating the alarm
firstFrame = None
gun_exist = False
alarm_active = False
frames_since_detection = 0

# Initialize the pygame module and load the alarm sound
pygame.init()
alarm_sound = pygame.mixer.Sound('alarm.wav')

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="face_detection.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the known faces from the directory and store their names in a list
known_names = []

for file in os.listdir(KNOWN_FACES_DIR):
    known_names.append(file.split('.')[0])

# Loop over the frames from the camera
while True:

    # Read the frame from the camera and resize it
    ret, frame = camera.read()
    frame = imutils.resize(frame, width=500)

    # Convert the frame to grayscale and detect guns using the cascade classifier
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

    # Set a flag if a gun is detected and draw a rectangle around the gun
    if len(gun) > 0:
        gun_exist = True
        frames_since_detection += 1
        if not alarm_active:
            alarm_sound.play()
            alarm_active = True
        if frames_since_detection > 10:
            screenshot = "screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email('Threat detected', 'Please check the attached screenshot', screenshot)
            frames_since_detection = 0
    else:
        gun_exist = False
        frames_since_detection = 0
        if alarm_active:
            alarm_sound.stop()
            alarm_active = False

    for (x, y, w, h) in gun:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    # Use sound detection to detect unusual sounds and send an email with an attached audio file if a sound is detected
    data, fs = sd.read(frames=1024, samplerate=44100, channels=1)
    rms = np.sqrt(np.mean(np.square(data)))
    if rms > SOUND_THRESHOLD:
        print("Unusual sound detected")
        filename = "sound.wav"
        sf.write(filename, data, fs)
        send_email('Unusual sound detected', 'Please check the attached audio file', filename)
        frames_since_detection = 0
        if not alarm_active:
            alarm_sound.play()
            alarm_active = True

    # Use the TFLite model to detect faces
    # Resize the frame and convert it to RGB
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Prepare the input image for the TFLite model
    input_data = np.expand_dims(rgb_small_frame, axis=0)
    input_data = (np.float32(input_data) - 127.5) / 127.5

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run the model
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Loop over the detected faces and compare them to the known faces
    for i in range(len(output_data)):
        face = output_data[i]

        # If the face is not recognized, activate the alarm and send an email
        if face[4] < 0.5:
            print("Unknown face detected")
            if not alarm_active:
                alarm_sound.play()
                alarm_active = True
                screenshot = "screenshot.jpg"
                cv2.imwrite(screenshot, frame)
                send_email('Unknown face detected', 'Please check the attached screenshot', screenshot)
                frames_since_detection = 0

                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                cv2.imshow("Security Feed", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                if key == ord('s'):
                    if alarm_active:
                        alarm_sound.stop()
                        alarm_active = False

    def send_email(subject, body, attachment=None):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            message = MIMEMultipart()
            message['From'] = EMAIL_ADDRESS
            message['To'] = EMAIL_ADDRESS
            message['Subject'] = subject

            if attachment:
                with open(attachment, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name

                file = MIMEApplication(file_data, Name=file_name)
                file['Content-Disposition'] = f'attachment; filename="{file_name}"'
                message.attach(file)

            text = MIMEText(body)
            message.attach(text)

            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
            print('Email sent successfully')
        except Exception as e:
            print(f'Error sending email: {e}')
            
            camera.release()
            cv2.destroyAllWindows()
            pygame.quit()