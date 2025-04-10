# Sistema de Detección y Control de Objetos con Brazo Robótico

Este proyecto implementa un sistema de visión por computadora que detecta objetos cuadrados de color rojo y controla un brazo robótico según la posición del objeto detectado. El sistema está desarrollado para Raspberry Pi y utiliza una cámara web para la detección.

## Características

- Detección de objetos cuadrados de color rojo en tiempo real
- División del campo de visión en tres zonas (izquierda, centro, derecha)
- Control de un brazo robótico con tres servomotores
- Interfaz web para visualización en tiempo real
- Movimientos suaves y controlados de los servomotores

## Requisitos

### Hardware
- Raspberry Pi
- Cámara web compatible
- 3 Servomotores
- Placa de control para servomotores
- Fuente de alimentación adecuada

### Software
- Python 3.x
- OpenCV (cv2)
- Flask
- RPi.GPIO
- NumPy

## Instalación

1. Instalar las dependencias necesarias:
```bash
pip install flask opencv-python numpy RPi.GPIO
```

2. Conectar los servomotores a los pines GPIO:
   - Servo Base: Pin 15
   - Servo Altura: Pin 13
   - Servo Garra: Pin 11

3. Asegurarse de que la cámara web esté conectada y configurada correctamente

## Uso

1. Ejecutar la aplicación:
```bash
python app.py
```

2. Abrir un navegador web y acceder a:
```
http://localhost:5000
```

3. La interfaz web mostrará:
   - La transmisión en vivo de la cámara
   - Las zonas de detección (izquierda, centro, derecha)
   - Los objetos detectados marcados con rectángulos verdes

## Funcionamiento

1. El sistema detecta objetos cuadrados de color rojo en tiempo real
2. Cuando se detecta un objeto, se determina en qué zona se encuentra:
   - Zona Izquierda: El brazo se mueve a la posición 1
   - Zona Centro: El brazo se mueve a la posición 2
   - Zona Derecha: El brazo se mueve a la posición 3
3. Después de cada movimiento, el brazo regresa a su posición neutral

## Notas Importantes

- Los servomotores se mueven de manera gradual para evitar movimientos bruscos
- El sistema está optimizado para detectar objetos cuadrados de color rojo
- Se recomienda una buena iluminación para una mejor detección
- Los valores de los servomotores pueden necesitar ajustes según el hardware específico

## Demostración

![Demostración del Sistema](https://i.imgur.com/D18UYN0.gif)