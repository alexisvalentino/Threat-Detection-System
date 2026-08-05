

# Sistema de Seguridad de Detección de Amenazas con Reconocimiento Facial, Detección de Armas y Capacidades de Análisis de Audio
Este sistema de seguridad está diseñado para reconocer tanto **amenazas conocidas** **(Entrenado para detectar y alertar sobre individuos específicos que puedan representar una amenaza, como aquellos en una lista de vigilancia o con antecedentes penales.)** como **rostros no identificados (Adecuado para entornos controlados donde el acceso está restringido únicamente al personal autorizado)**, permitiendo al personal de seguridad tomar las acciones adecuadas basándose en los individuos detectados. También es capaz de reconocer **rostros de los propietarios del hogar y el sistema no activa la alarma**. Además, cuenta con las capacidades de **detectar armas** e **identificar sonidos inusuales**. Cuando se detecta cualquiera de estos eventos, se activa una alarma y se envía una notificación por correo electrónico con las imágenes o archivos de audio correspondientes.

<h2>Dependencias</h2>
<p>Para ejecutar el script, debes instalar los siguientes paquetes de Python:</p>
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

<h2>Configuración</h2>
<p>Antes de ejecutar el script, también debes descargar, entrenar o configurar lo siguiente:</p>
<ul>
  <li>face_cascade.xml: un clasificador Haar Cascade preentrenado para detección de rostros.</li>
  <li>openface_nn4.small2.v1.t7: un modelo de red neuronal profunda preentrenado para reconocimiento facial.</li>
  <li> known_faces.pkl: un archivo pickle que contiene un diccionario de amenazas conocidas (nombre y embeddings).</li>
  <li>home_owners.pkl: un archivo pickle que contiene un diccionario de rostros de propietarios (nombre y embeddings).</li>
  <li>deploy.prototxt y res10_300x300_ssd_iter_140000_fp16.caffemodel: modelos de redes neuronales profundas preentrenados para detección de rostros utilizando el módulo DNN de OpenCV.</li>
  <li>ingresa tus credenciales de correo electrónico y las rutas a los archivos mencionados anteriormente en el código.</li>
</ul>

<h2>Cómo Funciona</h2>
<p>El código ejecuta un bucle infinito que captura fotogramas de la cámara web y realiza las siguientes operaciones:</p>
<ol>
  <li>Detección de armas: Utiliza un clasificador cascade preentrenado para detectar armas en el fotograma. Si se detecta un arma, el sistema activa una alarma y envía una notificación por correo electrónico con una captura de pantalla del fotograma.</li>
  <li>Detección y reconocimiento facial: Utiliza un clasificador Haar Cascade preentrenado para detección de rostros y el modelo de red neuronal profunda de OpenFace para reconocimiento facial, con el fin de detectar y reconocer rostros en el fotograma. Si se detecta el rostro de un propietario, el sistema no activa ninguna alarma. Si se detecta un rostro desconocido o una amenaza conocida, el sistema activa una alarma y envía una notificación por correo electrónico con una captura de pantalla del fotograma.</li>
  <li>Detección de audio: Utiliza la biblioteca sounddevice para capturar datos de audio desde el micrófono. Si se detecta cualquier sonido inusual, el sistema activa una alarma y envía una notificación por correo electrónico con una grabación del audio.</li>
  <li>Notificación por correo electrónico: Utiliza las bibliotecas nativas de Python email y smtplib para enviar notificaciones por correo electrónico con imágenes o archivos de audio adjuntos.</li>
  <li>El sistema también utiliza la biblioteca Pygame para reproducir un sonido de alarma cuando se activa esta.</li>
</ol>
  
 <h2>Ejecución del Script</h2>
 <p>Para ejecutar el script, simplemente ejecuta el archivo Python en tu terminal o símbolo del sistema:</p>
<p>El script comenzará a capturar video y audio, y activará alarmas y enviará notificaciones por correo electrónico cuando se detecten eventos.</p>

**Este sistema de detección de amenazas en tiempo real puede ser útil para aplicaciones de seguridad y vigilancia en el hogar. El código puede personalizarse para agregar más funcionalidades y mejorar la precisión de los modelos de detección.**
