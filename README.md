# Real-Time-Threat-Detection
This is a Python script that uses computer vision and machine learning techniques to detect weapons and unrecognized faces in a video stream. It also detects unusual sounds and sends email notifications with attached screenshots or audio files.
<h1>Installation</h1>
<p>To run this script, you need to have Python 3 installed on your system. You also need to install the following libraries:</p>
<ul>
<li>numpy</li>
<li>OpenCV</li>
<li>imutils</li>
<li>smtplib</li>
<li>datetime</li>
<li>pygame</li>
<li>sounddevice</li>
<li>soundfile</li>
<li>face_recognition</li>
</ul>
<p>'You can install these libraries using pip'</p>
<h1>Usage</h1>
<p>To use this script, you need to run it from the command line: <em>'python Detection.py'</em></p>
<p>The script will start the camera and display the video stream on the screen. It will detect guns and unrecognized faces in the stream and play an alarm sound if any are detected. It will also send email notifications with attached screenshots or audio files.</p>

<p>You can press the 'q' key to exit the script. You can also press the 's' key to stop the alarm sound if it's active.</p>
<h1>Configuration</h1>
<p>Before running the script, you need to configure some constants in the code:</p>
<ul>
<li>EMAIL_ADDRESS: The email address to use for sending notifications.</li>
<li>EMAIL_PASSWORD: The password for the email address.</li>
<li>KNOWN_FACES_DIR: The directory where known faces are stored.</li>
<li>SOUND_THRESHOLD: The threshold for detecting unusual sounds.</li>
</ul>
<p>You also need to put some known faces in the KNOWN_FACES_DIR directory. Each face should be in a separate image file with the person's name as the file name (e.g. john.jpg).</p>
<h1>License</h1>
<p>This script is licensed under the MIT License. See the LICENSE file for details.</p>

