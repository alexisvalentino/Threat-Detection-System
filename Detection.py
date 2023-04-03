import numpy as np
import cv2
import imutils
import smtplib
import datetime
import pygame
import sounddevice as sd
import soundfile as sf
import face_recognition

EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS'
EMAIL_PASSWORD = 'YOUR_EMAIL_PASSWORD'
KNOWN_FACES_DIR = 'known_faces'
SOUND_THRESHOLD = 0.05

gun_cascade = cv2.CascadeClassifier('cascade.xml')
camera = cv2.VideoCapture(0)

firstFrame = None
gun_exist = False
alarm_active = False
frames_since_detection = 0

pygame.init()
alarm_sound = pygame.mixer.Sound('alarm.wav')

known_faces = []
known_names = []

for file in os.listdir(KNOWN_FACES_DIR):
    image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, file))
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(file.split('.')[0])

def send_email(subject, body, attachment=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        message = f'Subject: {subject}\n\n{body}'

        if attachment:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                file_name = f.name

            message = MIMEMultipart()
            message['From'] = EMAIL_ADDRESS
            message['To'] = EMAIL_ADDRESS
            message['Subject'] = subject

            file = MIMEApplication(file_data, Name=file_name)
            file['Content-Disposition'] = f'attachment; filename="{file_name}"'
            message.attach(file)

            text = MIMEText(body)
            message.attach(text)

            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
        else:
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {e}')

while True:

    ret, frame = camera.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

    if len(gun) > 0:
        gun_exist = True
    else:
        gun_exist = False

    for (x, y, w, h) in gun:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    if firstFrame is None:
        firstFrame = gray
        continue

    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if gun_exist:
        print("guns detected")
        frames_since_detection += 1
        if not alarm_active:
            alarm_sound.play(-1)
        alarm_active = True
    else:
        print("guns NOT detected")
        frames_since_detection = 0
        if alarm_active:
            alarm_sound.stop()
        alarm_active = False

    if frames_since_detection > 10:
        screenshot = "screenshot.jpg"
        cv2.imwrite(screenshot, frame)
        send_email('Threat detected', 'Please check the attached screenshot', screenshot)
        frames_since_detection = 0

    if key == ord('s'):
        if alarm_active:
            alarm_sound.stop()
        alarm_active = False

    # Face recognition
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        if name == "Unknown":
            print("Unrecognized face detected")
            screenshot = "screenshot.jpg"
            cv2.imwrite(screenshot, frame)
            send_email('Threat detected', 'Please check the attached screenshot', screenshot)
            _since_detection = 0
            if alarm_active:
                alarm_sound.stop()
            alarm_active = False
            send_email('Unrecognized face detected', 'Please check the attached screenshot', screenshot)

    # Sound detection
    data, fs = sd.read(frames=1024, samplerate=44100, channels=1)
    rms = np.sqrt(np.mean(np.square(data)))
    if rms > SOUND_THRESHOLD:
        print("Unusual sound detected")
        filename = "sound.wav"
        sf.write(filename, data, fs)
        send_email('Unusual sound detected', 'Please check the attached audio file', filename)
        frames_since_detection = 0
        if alarm_active:
            alarm_sound.stop()
        alarm_active = False

camera.release()
cv2.destroyAllWindows()
pygame.quit()
