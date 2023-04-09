# Real Time Threat Detection
This is a Python script that performs security surveillance using a camera. The code imports several libraries including NumPy, OpenCV (cv2), Imutils, pygame, sounddevice, and soundfile. It also imports the smtplib, datetime, and os libraries to send email notifications, obtain the current date and time, and access the operating system, respectively. TensorFlow (tf) is imported to perform face detection using a pre-trained model.

The script first sets the email address and password for the email account that will be used to send notifications, the directory where the known faces are stored, and the sound threshold for detecting unusual sounds. It then loads the cascade classifier for detecting guns and starts the camera.

The script initializes variables for detecting guns and activating the alarm and loads the alarm sound. It then loads the TFLite model and gets the input and output tensors.

Next, the script loads the known faces from the directory and stores their names in a list. It then loops over the frames from the camera, reads and resizes each frame, converts the frame to grayscale and detects guns using the cascade classifier. If a gun is detected, a flag is set, a rectangle is drawn around the gun, and an alarm is activated. If a gun is detected for more than 10 frames, a screenshot is taken, an email is sent with the screenshot attached, and the frames since detection is reset.

The script then uses sound detection to detect unusual sounds and sends an email with an attached audio file if a sound is detected. The frames since detection is reset, and an alarm is activated if it is not already active.

Finally, the script uses the TFLite model to detect faces, compares them to the known faces, and activates the alarm and sends an email if an unknown face is detected.

<h2>Requirements</h2>
<ul>
  <li>Python 3.6 or higher</li>
  <li>OpenCV (cv2)imutils</li>
  <li>imutils</li>
  <li>numpy</li>
  <li>smtplib</li>
  <li>datetime</li>
  <li>pygame</li>
  <li>sounddevice</li>
  <li>soundfile</li>
  <li>tensorflow</li>
</ul>

<h2>Installation</h2>
<ol>
  <li>Clone the repository to your local machine.</li>
  <li>Install the required packages by running pip install -r requirements.txt in the command line.</li>
  <li>Download the cascade.xml file for detecting guns from <a href="https://drive.google.com/file/d/1Ndr_HFhxHB8mJ_uysdasXgfAKSQ2is4q/view">here.</a></li>
  <li>Train your own face_detection.tflite file for face detection from <a href="https://www.tensorflow.org/js/models">here.</a></li>
  <li>Put the cascade.xml and face_detection.tflite files in the same directory as the Python script.</li>
</ol>

<h2>Usage</h2>
<ol>
  <li>Set the email address and password for the email account that will be used to send notifications by updating the EMAIL_ADDRESS and EMAIL_PASSWORD variables.</li>
  <li>Put the known faces in the known_faces directory.</li>
  <li>Run the Python script by typing python security_system.py in the command line.</li>
</ol>
  
 <h2>Features</h2>
 <p>The security system has the following features:</p>
 <ul>
  <li>Detects guns in the video feed using the Haar Cascade classifier and sends an email with a screenshot if a gun is detected.</li>
  <li>Detects unusual sounds in the audio feed and sends an email with an attached audio file if a sound is detected.</li>
  <li>Detects faces in the video feed using a TFLite model and compares them to the known faces. If an unknown face is detected, the system activates an alarm and sends an email with a screenshot.</li>
</ul>
 
