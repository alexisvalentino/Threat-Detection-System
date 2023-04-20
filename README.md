# Threat Detection Security System with Face Recognition, Gun Detection, and Audio Analysis Capabilities
This security system is designed to recognize both **Known threats** **(Trained to detect and alert for specific individuals that may pose a threat, such as those on a watchlist or individuals with a history of criminal activity.)** and **Unidentified faces (Suitable for controlled environments where access is restricted to authorized personnel only)** allowing security personnel to take appropriate actions based on the detected individuals, It's also able to recognize **home owner faces and the system does not trigger an alarm.** It has also the capabilities of **Detecting guns**, and **Identifying unusual sounds**. When any of these events are detected, an alarm is triggered and an email notification is sent with relevant images or audio files.

<h2>Dependencies</h2>
<p>To run the script, you need to install the following Python packages:</p>
<ul>
  <li>numpy</li>
  <li>opencv-python</li>
  <li>imutils</li>
  <li>pygame</li>
  <li>smtplib</li>
  <li>sounddevice</li>
  <li>scipy</li>
  <li>pickle</li>
</ul>

<h2>Configuration</h2>
<p>Before running the script, You also need to download or train and configure the following:</p>
<ul>
  <li>face_cascade.xml: a pre-trained Haar Cascade classifier for face detection.</li>
  <li>openface_nn4.small2.v1.t7: a pre-trained deep neural network model for face recognition.</li>
  <li> known_faces.pkl: a pickle file containing a dictionary of known threats (name and embeddings).</li>
  <li>home_owners.pkl: a pickle file containing a dictionary of homeowner faces (name and embeddings).</li>
  <li>deploy.prototxt and res10_300x300_ssd_iter_140000.caffemodel: pre-trained deep neural network models for face detection using OpenCV’s DNN module.</li>
  <li>enter your email credentials and the paths to the above-mentioned files in the code.</li>
</ul>

<h2>How It Works</h2>
<p>The code runs an infinite loop that captures frames from the webcam and performs the following operations:</p>
<ol>
  <li>Gun detection: Uses a pre-trained cascade classifier to detect guns in the frame. If a gun is detected, the system triggers an alarm and sends an email notification with a screenshot of the frame.</li>
  <li>Face detection and recognition: Uses a pre-trained Haar Cascade classifier for face detection and OpenFace’s deep neural network model for face recognition to detect and recognize faces in the frame. If a homeowner face is detected, the system does not trigger any alarm. If an unknown face or known threats is detected, the system triggers an alarm and sends an email notification with a screenshot of the frame.</li>
  <li>Audio detection: Uses sounddevice library to capture audio data from the microphone. If any unusual sound is detected, the system triggers an alarm and sends an email notification with a recording of the audio.</li>
  <li>Email notification: Uses Python’s built-in email and smtplib libraries to send email notifications with attached images or audio files.</li>
  <li>The system also uses the Pygame library to play an alarm sound when an alarm is triggered.</li>
</ol>
  
 <h2>Running the Script</h2>
 <p>To run the script, simply execute the Python file in your terminal or command prompt:</p>
<p>The script will start capturing video and audio, and it will trigger alarms and send email notifications when events are detected.</p>

**This real-time threat detection system can be useful for home security and surveillance applications. The code can be customized to add more functionalities and improve the accuracy of the detection models.**
 
