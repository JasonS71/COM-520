from flask import Flask, Response
import cv2
import threading
import time
import os
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import curses

app = Flask(__name__)

frame = None
lock = threading.Lock()

# Configuracin de pines (igual que antes)
SERVO_BASE = 15
SERVO_ALTURA = 13
SERVO_GARRA = 11

GPIO.cleanup()

# Configuracin inicial
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_BASE, GPIO.OUT)
GPIO.setup(SERVO_ALTURA, GPIO.OUT)
GPIO.setup(SERVO_GARRA, GPIO.OUT)

# Inicializar PWM
pwm_base = GPIO.PWM(SERVO_BASE, 50)
pwm_altura = GPIO.PWM(SERVO_ALTURA, 50)
pwm_garra = GPIO.PWM(SERVO_GARRA, 50)

# Variables para almacenar los valores actuales
current_base = 7.5  # Valor neutral tpico (90)
current_altura = 7.5
current_garra = 9.0

pwm_base.start(current_base)
pwm_altura.start(current_altura)
pwm_garra.start(current_garra)

def detectar_cuadrados_rojos(frame):
    # Convertir la imagen de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rango para el color rojo (se usan dos rangos por la envoltura del tono en HSV)
    rojo_bajo1 = np.array([0, 120, 70])
    rojo_alto1 = np.array([10, 255, 255])
    rojo_bajo2 = np.array([170, 120, 70])
    rojo_alto2 = np.array([180, 255, 255])
    
    # Crear la mscara para el rojo
    mask1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
    mask2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
    mask = mask1 + mask2

    # Opcional: aplicar un poco de suavizado para reducir ruido
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Encontrar contornos en la mscara
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cuadrados = []
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        # Filtrar por rea mnima para ignorar falsos positivos
        if area > 500:
            # Aproximar la forma del contorno
            perimetro = cv2.arcLength(cnt, True)
            aprox = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
            
            # Si tiene 4 vrtices, podra ser un cuadrado o rectngulo
            if len(aprox) == 4:
                # Obtener el rectngulo delimitador
                x, y, w, h = cv2.boundingRect(aprox)
                # Se puede aadir un criterio de aspecto para confirmar que es cuadrado
                aspecto = float(w) / h
                if 0.8 <= aspecto <= 1.2:
                    cuadrados.append((x, y, w, h))
    return cuadrados
    
def determinar_zona(x, ancho_cuadro, ancho_frame):
    # Se calcula el centro del cuadrado en x
    centro = x + ancho_cuadro / 2
    # Se definen los lmites de las tres zonas
    limite_izq = ancho_frame / 3
    limite_der = 2 * ancho_frame / 3
    
    if centro < limite_izq:
        return "IZQUIERDA"
    elif centro > limite_der:
        return "DERECHA"
    else:
        return "CENTRO"
        
def gradual_change(pwm, current, target, step=0.1, delay=0.05):
    if current < target:
        values = np.arange(current, target, step)
    else:
        values = np.arange(current, target, -step)
    
    for value in values:
        pwm.ChangeDutyCycle(value)
        sleep(delay)
    # Asegurarse de establecer el valor final exacto
    pwm.ChangeDutyCycle(target)
    sleep(delay)
    return target

# Funciones para mover los servomotores segn la zona detectada
def zone_1():
    global current_base, current_altura, current_garra
    # Valores para la zona 1: Base = 4.9, Altura = 10.5
    target_base = 4.9
    target_altura = 10.5
    target_garra = 4.5  # Valor neutral para la garra

    current_base = gradual_change(pwm_base, current_base, target_base)
    current_altura = gradual_change(pwm_altura, current_altura, target_altura)
    current_garra = gradual_change(pwm_garra, current_garra, target_garra)
    
    print("Ejecutando zone_1: Base =", current_base, "Altura =", current_altura)
    neutral_base = 7.5
    neutral_altura = 7.5
    neutral_garra = 9.0
    current_base = gradual_change(pwm_base, current_base, neutral_base)
    current_altura = gradual_change(pwm_altura, current_altura, neutral_altura)
    current_garra = gradual_change(pwm_garra, current_garra, neutral_garra)
    
    print("Regresando a valores iniciales: Base =", current_base, "Altura =", current_altura)

def zone_2():
    global current_base, current_altura, current_garra
    # Valores para la zona 2: Base = 7, Altura = 10.5
    target_base = 7
    target_altura = 10.5
    target_garra = 4.5  # Valor neutral para la garra
    
    current_base = gradual_change(pwm_base, current_base, target_base)
    current_altura = gradual_change(pwm_altura, current_altura, target_altura)
    current_garra = gradual_change(pwm_garra, current_garra, target_garra)
    
    print("Ejecutando zone_2: Base =", current_base, "Altura =", current_altura)
    neutral_base = 7.5
    neutral_altura = 7.5
    neutral_garra = 9.0
    current_base = gradual_change(pwm_base, current_base, neutral_base)
    current_altura = gradual_change(pwm_altura, current_altura, neutral_altura)
    current_garra = gradual_change(pwm_garra, current_garra, neutral_garra)
    
    print("Regresando a valores iniciales: Base =", current_base, "Altura =", current_altura)

# La funcin zone_3 se deja vaca o se puede definir si se requiere para otra accin.
def zone_3():
    global current_base, current_altura, current_garra
    # Valores para la zona 2: Base = 7, Altura = 10.5
    target_base = 8.5
    target_altura = 10.5
    target_garra = 4.5  # Valor neutral para la garra
    
    current_base = gradual_change(pwm_base, current_base, target_base)
    current_altura = gradual_change(pwm_altura, current_altura, target_altura)
    current_garra = gradual_change(pwm_garra, current_garra, target_garra)
    
    print("Ejecutando zone_3: Base =", current_base, "Altura =", current_altura)
    neutral_base = 7.5
    neutral_altura = 7.5
    neutral_garra = 9.0
    current_base = gradual_change(pwm_base, current_base, neutral_base)
    current_altura = gradual_change(pwm_altura, current_altura, neutral_altura)
    current_garra = gradual_change(pwm_garra, current_garra, neutral_garra)
    
    print("Regresando a valores iniciales: Base =", current_base, "Altura =", current_altura)

def capture_camera():
    global frame
    global processing_zone
    camera = cv2.VideoCapture(0)
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 250)
    
    while True:
        success, img = camera.read()
        if success:
            processing_zone = False
            alto_frame, ancho_frame = img.shape[:2]
        
            # Detectar cuadrados rojos en la imagen
            cuadrados = detectar_cuadrados_rojos(img)
        
            # Dibujar las zonas en la imagen (lneas divisorias)
            cv2.line(img, (int(ancho_frame/3), 0), (int(ancho_frame/3), alto_frame), (255, 255, 255), 2)
            cv2.line(img, (int(2*ancho_frame/3), 0), (int(2*ancho_frame/3), alto_frame), (255, 255, 255), 2)
        
            # Verificar si se detecta algn cuadrado rojo
            if cuadrados and not processing_zone:
                processing_zone = True
                # Se toma el primer cuadrado detectado para determinar la zona
                x, y, w, h = cuadrados[0]
                zona = determinar_zona(x, w, ancho_frame)
            
                # Dibujar el rectngulo y la etiqueta de la zona para este cuadrado
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, zona, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
                # Mover los servomotores segn la zona detectada
                if zona == "CENTRO":
                    zone_2()
                elif zona == "IZQUIERDA":
                    zone_1()
                else:
                    zone_3()
                    
                processing_zone = False
            with lock:
                frame = img.copy()
        else:
            print("Error al leer de la cmara")
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
