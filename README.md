# Security System with Face Recognition, Gun Detection, and Unusual Sound Detection
This security system is designed to recognize both **Known faces** **(intended to detect and alert for specific individuals that may pose a threat, such as those on a watchlist or individuals with a history of criminal activity.)** and **Unknown faces (suitable for controlled environments where access is restricted to authorized personnel only)** allowing security personnel to take appropriate actions based on the detected individuals,  **Detect guns**, and **Identify unusual sounds**. When any of these events are detected, an alarm is triggered and an email notification is sent with relevant images or audio files.

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
</ul>

<p>Install them using the following command:</p>
`pip install numpy opencv-python imutils pygame smtplib sounddevice scipy`

<h2>Configuration</h2>
<p>Before running the script, you need to configure the following variables:</p>
<ul>
  <li>`email`: Your Gmail address.</li>
  <li>`password`: Your Gmail password.</li>
  <li>`receiver_email`: The email address where notifications will be sent.</li>
  <li>`haar_cascade_path`: The path to the Haar Cascade XML file for face detection.</li>
  <li>`known_faces_model_path`: The path to the known faces model (pickle file).</li>
  <li>`protoPath`: The path to the deploy.prototxt file for the DNN face detector.</li>
  <li>`modelPath`: The path to the res10_300x300_ssd_iter_140000.caffemodel file for the DNN face detector.</li>
  <li>`embedder_model_path`: The path to the openface_nn4.small2.v1.t7 file for the DNN face recognizer.</li>
</ul>

<h2>How It Works</h2>
<p>The script continuously captures video frames from a camera and performs the following tasks:</p>
<ol>
  <li>Face Detection: The script detects faces using Haar Cascade and checks if they are known faces or unknown faces. Known faces are loaded from a pre-trained model, and their embeddings are compared to the detected face's embedding. If a known face is detected, it draws a green rectangle around it and displays the name. For unknown faces, a red rectangle is drawn.</li>
  <li>Gun Detection: The script detects guns in the video frames. If a gun is detected, it draws a blue rectangle around it.</li>
  <li>Unusual Sound Detection: The script continuously records audio and checks for unusual sounds. If an unusual sound is detected, it saves the audio clip as a WAV file.</li>
  <li>Alarms and Email Notifications: When a known face, unknown face, gun, or unusual sound is detected, the script plays an alarm for 10 seconds and sends an email notification with an attached image or audio file.</li>
</ol>
  
 <h2>Running the Script</h2>
 <p>To run the script, simply execute the Python file in your terminal or command prompt:</p>
<p>` python security_system.py`</p>
<p>The script will start capturing video and audio, and it will trigger alarms and send email notifications when events are detected.</p>
 
