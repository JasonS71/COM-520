# Proyecto: Vehículo con Raspberry Pi

## Descripción del Proyecto

El proyecto consiste en un vehículo de pequeña escala que utiliza una Raspberry Pi como unidad de procesamiento principal. El sistema está diseñado para controlar motores mediante un driver especializado, permitiendo el movimiento preciso del vehículo.

## Componentes del Sistema

- Raspberry Pi (unidad de control)
- Tarjeta Micro SD (V30 y U3 recomendada)
- 2 Drivers Motoron M3H550 para control de motores
- 4 Motores JGB37-520 (motores con encoder)
- Chasis para montaje de componentes
- Fuente de alimentación (10V para motores, 5V para Raspberry Pi)
- Cableado para interconexiones

## Estructura del Proyecto

El proyecto se divide en tres secciones principales:

1. Implementación del sistema operativo en Raspberry Pi
2. Diseño y configuración de conexiones físicas
3. Desarrollo e implementación del código de control

## 1. Implementación del Sistema Operativo en Raspberry Pi

Esta sección documenta el proceso de instalación y configuración del sistema operativo Raspberry Pi OS, necesario para el funcionamiento del vehículo.

### Especificaciones de Almacenamiento

Para un buen rendimiento del sistema, se recomienda usar una tarjeta Micro SD con estas características:

- **Clasificación de rendimiento**: V30 y U3
- **Capacidad mínima recomendada**: 16GB

![Especificaciones Micro SD](img/Micro%20SD%20Card.png)

La elección de una tarjeta SD de alto rendimiento mejorará la velocidad de respuesta del sistema. Estas son las diferentes clasificaciones de velocidad:

![Clasificación de Velocidades SD](img/SD%20Card%20Speed.png)

### Proceso de Instalación del Sistema

#### 1. Instalación de Raspberry Pi Imager
Para comenzar, es necesario instalar el software oficial para grabar el sistema operativo:

- Descargar Raspberry Pi Imager desde: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)
- El software funciona en Windows, macOS y Linux

![Software Raspberry Pi Imager](img/Instalacion%20Raspberry%201.png)

#### 2. Formateo de la Tarjeta SD
Preparación de la tarjeta SD para instalar el sistema operativo:

- Conectar la tarjeta SD a la computadora
- Usar la opción de formateo en Raspberry Pi Imager

![Proceso de Formateo](img/Instalacion%20Raspberry%202.png)

#### 3. Configuración de SSH
Configuración del acceso remoto mediante SSH:

- En las opciones avanzadas de Raspberry Pi Imager, habilitar SSH
- Esto permitirá controlar el Raspberry Pi de forma remota

![Configuración SSH](img/Instalacion%20Raspberry%203.png)

#### 4. Configuración de WiFi
Configuración de la conexión inalámbrica para que funcione automáticamente:

- Introducir los datos de la red WiFi desde las opciones avanzadas
- El Raspberry Pi se conectará automáticamente a esta red al iniciar

![Configuración WiFi](img/Instalacion%20Raspberry%204.png)

#### 5. Selección del Sistema Operativo
Elegir el sistema operativo adecuado para el proyecto:

- Se recomienda Raspberry Pi OS (32-bit)
- Esta versión es compatible con las bibliotecas y drivers necesarios para el proyecto

![Selección de Sistema Operativo](img/Instalacion%20Raspberry%205.png)

#### 6. Selección de la Tarjeta SD
Indicación del dispositivo donde instalar el sistema:

- Seleccionar la tarjeta SD correcta en la lista
- Verificar que no haya datos importantes en ella, ya que serán borrados

![Selección de Dispositivo](img/Instalacion%20Raspberry%206.png)

#### 7. Escritura del Sistema
Instalación del sistema operativo en la tarjeta SD:

- Hacer clic en "Escribir" y esperar a que termine el proceso
- El tiempo varía según la velocidad de la tarjeta SD

![Proceso de Instalación](img/Instalacion%20Raspberry%207.png)

#### 8. Inserción de la Tarjeta SD
Colocación de la tarjeta en el Raspberry Pi:

- Retirar la tarjeta SD de la computadora con seguridad
- Insertar en la ranura correspondiente del Raspberry Pi

![Instalación Física de SD](img/Instalacion%20Raspberry%208.png)

#### 9. Conexión de Alimentación
Provisión de energía al sistema:

- Conectar un cable micro USB o USB-C (según el modelo) al Raspberry Pi
- Usar una fuente de alimentación de 5V y 2.5A para mejor estabilidad

![Conexión de Alimentación](img/Instalacion%20Raspberry%209.png)

#### 10. Conexión Remota con VNC Viewer
Configuración del acceso remoto para controlar el Raspberry Pi:

- Descargar VNC Viewer desde [https://www.realvnc.com/en/connect/download/viewer/](https://www.realvnc.com/en/connect/download/viewer/)
- Asegurar que la computadora y el Raspberry Pi estén en la misma red WiFi
- Averiguar la dirección IP del Raspberry Pi usando herramientas como Advanced IP Scanner
- Introducir esta IP en VNC Viewer para conectarse

**Nota importante**: La computadora y el Raspberry Pi deben estar en la misma red WiFi para poder establecer la conexión.

![Configuración VNC](img/Instalacion%20Raspberry%2010.png)

#### 11. Ingreso de Credenciales
Acceso al sistema:

- Ingresar el usuario y contraseña configurados
- Si no fueron modificados, las credenciales por defecto son:
  - Usuario: pi
  - Contraseña: raspberry

![Proceso de Autenticación](img/Instalacion%20Raspberry%2011.png)

#### 12. Acceso al Escritorio
Finalización del proceso:

- Una vez conectado, se visualizará el escritorio de Raspberry Pi OS
- Ahora es posible controlar el Raspberry Pi de forma remota

![Entorno de Trabajo](img/Instalacion%20Raspberry%2012.png)

Con la instalación del sistema operativo completada, el Raspberry Pi está listo para la siguiente fase: la integración con los componentes físicos del vehículo.

## 2. Diseño y configuración de conexiones físicas

Esta sección explica cómo conectar todos los componentes electrónicos del vehículo para su correcto funcionamiento.

### Componentes de movimiento y control

#### Motores JGB37-520

Los motores utilizados en este proyecto son del modelo JGB37-520, que incluyen encoders para el control preciso de movimiento.

![Motor JGB37-520](img/Motor%20JGB37-520.png)

Cada motor tiene 6 pines con las siguientes funciones:
- **Pines 1 y 6**: Control del motor (se conectan al driver)
- **Pines 2 y 5**: Alimentación del encoder
- **Pines 3 y 4**: Lectura de datos del encoder

#### Driver Motoron M3H550

Para controlar los motores, se utilizan drivers Motoron M3H550, que permiten manejar hasta 3 motores por placa.

![Driver Motoron](img/Driver%20Motoron%20M3H550.png)

Como el vehículo usa 4 motores, es necesario utilizar 2 drivers para poder controlarlos todos.

### Conexiones entre componentes

#### Conexión de los motores al driver

Cada motor se conecta al driver usando los pines 1 y 6 del motor a los pines correspondientes en el driver:

- Los pines del driver para los motores están etiquetados como: M1A, M1B, M2A, M2B, M3A y M3B
- Cada par (por ejemplo, M1A y M1B) controla un motor

#### Alimentación del sistema

El sistema requiere dos voltajes diferentes:

1. **Para los drivers Motoron**:
   - Los pines 3V3 y GND se utilizan para alimentar la electrónica del driver
   - **IMPORTANTE**: El driver solo funciona con 3.3V, no conectar a 5V o podría dañarse

2. **Para los motores**:
   - Los pines VIN y GND se utilizan para alimentar los motores
   - Para los motores JGB37-520 se requiere una alimentación de 10V

#### Montaje del driver en Raspberry Pi

La conexión del driver con el Raspberry Pi es muy sencilla:

- El driver Motoron M3H550 está diseñado para montarse directamente sobre el Raspberry Pi
- Solo es necesario alinear los pines GPIO del Raspberry Pi con los conectores del driver y presionar con cuidado

### Diagrama de conexiones

Para una mejor comprensión del sistema completo, se puede consultar el siguiente diagrama que muestra todas las conexiones entre los componentes:

![Diagrama de Conexiones](img/Diagrama%20de%20conexión.png)

## 3. Desarrollo e implementación del código de control

En esta sección se detalla el código necesario para controlar el vehículo utilizando los drivers Motoron y los motores con encoders.

### Repositorios y código fuente

Para este proyecto se utilizan dos repositorios:

1. **Repositorio principal del proyecto**:
   ```
   git clone https://github.com/JasonS71/COM-520
   ```
   Este repositorio contiene el código completo del curso COM-520, incluyendo el proyecto del vehículo.

2. **Biblioteca Motoron para control de drivers**:
   ```
   git clone https://github.com/pololu/motoron-python
   ```
   Esta biblioteca, desarrollada por Pololu, proporciona las funciones necesarias para controlar los drivers Motoron.

### Instalación de dependencias

Para el funcionamiento correcto del código, es necesario instalar las siguientes dependencias:

```
sudo apt update
sudo apt install python3-smbus2 python3-serial
```

### Estructura y ubicación del código

El archivo principal para el control del vehículo se encuentra en:
```
Examen_final/motoron-python/app.py
```

Este archivo contiene toda la lógica necesaria para la operación del vehículo, utilizando la biblioteca Motoron para comunicarse con los drivers.

#### Configuración de los encoders

Los encoders de los motores se configuran mediante la definición de sus pines GPIO en el Raspberry Pi. Esta configuración puede modificarse según las conexiones físicas realizadas:

```python
# Definición de pines de encoders
ENCODER_PINS = {
    'mc1_motor2': {'pin_a': 4, 'pin_b': 10, 'name': 'abajo_izquierda'},
    'mc1_motor3': {'pin_a': 18, 'pin_b': 17, 'name': 'arriba_izquierda'},
    'mc2_motor1': {'pin_a': 22, 'pin_b': 27, 'name': 'abajo_derecha'},
    'mc2_motor2': {'pin_a': 23, 'pin_b': 4, 'name': 'arriba_derecha'}
}
```

Esta configuración asocia cada motor con sus correspondientes pines de encoder y les asigna un nombre descriptivo según su ubicación en el vehículo.

#### Configuración de velocidades

Las velocidades de operación del vehículo se pueden ajustar modificando las siguientes constantes:

```python
# Velocidades de operación
BASE_SPEED = 400
TURN_SPEED = 300
```

- `BASE_SPEED`: Define la velocidad principal de avance del vehículo.
- `TURN_SPEED`: Define la velocidad durante los giros del vehículo.

Estos valores pueden requerir ajustes dependiendo de las características específicas del vehículo construido (peso, torque de los motores, tipo de superficie, etc.).

### Ejecución del código

Para ejecutar el código de control:

1. Acceder al directorio del proyecto:
   ```
   cd Examen_final/motoron-python
   ```

2. Ejecutar el archivo app.py:
   ```
   python3 app.py
   ```

### Modificaciones y personalización

El código proporciona una base funcional para el control del vehículo, pero puede ser modificado para adaptarse a necesidades específicas:

- Los pines de los encoders pueden cambiar según las conexiones físicas realizadas.
- Las velocidades pueden ajustarse para obtener un movimiento más rápido o más preciso.

