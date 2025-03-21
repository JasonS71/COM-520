from flask import Flask, Response
import cv2
import threading
import time
import os

app = Flask(__name__)

frame = None
lock = threading.Lock()

cascade_file = 'haarcascade_frontalface_default.xml'
if not os.path.isfile(cascade_file):
    print("Cargando Haarcascade desde la web")
    cascade_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(cascade_file)

def capture_camera():
    global frame
    camera = cv2.VideoCapture(0)
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        success, img = camera.read()
        if success:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                cv2.putText(img, 'Rostro', (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            with lock:
                frame = img.copy()
        else:
            print("Error al leer de la camara")
            time.sleep(1)
            camera = cv2.VideoCapture(0)  
            
        time.sleep(0.03) 
        
def generate_frames():
    global frame
    while True:
        with lock:
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                img_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
        time.sleep(0.03)
        
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Deteccion Facial - Raspberry Pi</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                margin-top: 20px;
                background-color: #f0f0f0;
            }
            h1 { 
                color: #2c3e50; 
                text-shadow: 1px 1px 2px #ccc;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            img { 
                max-width: 100%; 
                border: 3px solid #3498db; 
                border-radius: 5px; 
            }
            .info {
                margin-top: 20px;
                padding: 10px;
                background-color: #e8f4fc;
                border-radius: 5px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Deteccion Facial en Tiempo Real - Robotica 2</h1>
            <img src="/video_feed" />
            <div class="info">
                <p><strong>Estado:</strong> Streaming activo</p>
                <p><strong>Camara:</strong> USB Webcam</p>
                <p><strong>Detector:</strong> Haar Cascade - Frontal Face</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera_thread = threading.Thread(target=capture_camera)
    camera_thread.daemon = True
    camera_thread.start()
    
    print("Servidor iniciado en http://0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, threaded=True)