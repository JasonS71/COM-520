# 🚗 Control de Motores JGB37-520 con Raspberry Pi y Motoron

Este proyecto implementa el control de 4 motores JGB37-520 utilizando una Raspberry Pi 4 y controladores Motoron, montados sobre un chasis de perfiles de aluminio.

## 📋 Tabla de Contenidos

- [Componentes Necesarios](#-componentes-necesarios)
- [Configuración del Sistema](#️-configuración-del-sistema)
- [Instalación de Software](#-instalación-de-software)
- [Configuración de Hardware](#-configuración-de-hardware)
- [Conexiones](#-conexiones)
- [Pruebas](#-pruebas)
- [Troubleshooting](#-troubleshooting)

## 🔧 Componentes Necesarios

### Hardware Principal
- **Raspberry Pi 4** (4GB RAM)
- **4x Motores JGB37-520** con encoders
- **2x Controladores Motoron** (para control de motores DC)
- **Perfiles de aluminio** para el chasis
- **Fuente de alimentación** (1.8-22V DC para motores)
- **Cables de conexión** y jumpers

### Accesorios
- Tarjeta microSD (32GB recomendado)
- Cables duplex hembra-hembra
- Protoboard (opcional para conexiones)
- **Fuente de alimentación externa 220V AC a DC** (como se muestra en la imagen)

## 🖥️ Configuración del Sistema

### 1. Preparación de la Raspberry Pi

1. **Instalar Raspberry Pi OS** en la tarjeta microSD
2. **Habilitar SSH y VNC** durante la configuración inicial
3. **Conectar RealVNC** para control remoto:
   ```bash
   # En la Raspberry Pi, ejecutar:
   sudo raspi-config
   # Navegar a: Interface Options > VNC > Enable
   ```

### 2. Conexión Remota
- Utilizar **RealVNC Viewer** desde tu computadora
- Conectarse usando la IP de la Raspberry Pi
- Credenciales por defecto: `pi` / `raspberry` (cambiar por seguridad)

## 💻 Instalación de Software

### 1. Actualizar el Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Python y Dependencias
```bash
# Python ya viene preinstalado, verificar versión
python3 --version

# Instalar pip si no está disponible
sudo apt install python3-pip -y

# Instalar git
sudo apt install git -y
```

### 3. Habilitar I2C
```bash
# Método 1: Usando raspi-config
sudo raspi-config
# Navegar a: Interface Options > I2C > Enable

# Método 2: Editar directamente
sudo nano /boot/config.txt
# Agregar o descomentar: dtparam=i2c_arm=on

# Reiniciar el sistema
sudo reboot
```

### 4. Verificar I2C
```bash
# Instalar herramientas I2C
sudo apt install i2c-tools -y

# Detectar dispositivos I2C
sudo i2cdetect -y 1
```

### 5. Instalar Librería Motoron
```bash
# Clonar el repositorio oficial
git clone https://github.com/pololu/motoron-python.git

# Navegar al directorio
cd motoron-python

# Instalar la librería
sudo python3 setup.py install
```

## 🔌 Configuración de Hardware

### Configuración de Controladores Motoron

Los controladores Motoron deben configurarse con direcciones I2C únicas:

- **Controlador 1** (Ruedas Delanteras): Dirección `16` (0x10)
- **Controlador 2** (Ruedas Traseras): Dirección `17` (0x11)

### Proceso de Configuración:
1. Conectar cada controlador individualmente
2. Usar el software de configuración de Motoron
3. Asignar las direcciones correspondientes
4. Verificar con `sudo i2cdetect -y 1`

## 🔗 Conexiones

### Diagrama de Conexión

```
Raspberry Pi 4
├── Pin 3 (SDA) ──────┐
├── Pin 5 (SCL) ──────┤
├── Pin 6 (GND) ──────┤
└── Pin 2 (5V)  ──────┤
                      │
              ┌───────┴───────┐
              │   I2C Bus     │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   Motoron 1      Motoron 2         │
   (Addr: 16)     (Addr: 17)        │
        │             │             │
   ┌────┴────┐   ┌────┴────┐       │
   │ M1A+ M1A-│   │ M1A+ M1A-│       │
   │ M1B+ M1B-│   │ M1B+ M1B-│       │
   └────┬────┘   └────┬────┘       │
        │             │             │
  Motor FL&FR    Motor BL&BR        │
                                    │
              Fuente Externa 220V AC ──────┘
              (Adaptador a 1.8-22V DC)
```

![diagram](https://github.com/user-attachments/assets/c4c2c205-d4a0-4baa-b17d-3e9a3b48d765)

![Imagen de WhatsApp 2025-05-30 a las 01 44 41_f8fe1d7c](https://github.com/user-attachments/assets/7a6e9c9b-728f-41e7-b466-959451ddcd4f)

### Conexiones Detalladas

#### Raspberry Pi a Controladores Motoron:
| Raspberry Pi | Motoron 1 & 2 |
|--------------|---------------|
| Pin 3 (SDA)  | SDA           |
| Pin 5 (SCL)  | SCL           |
| Pin 6 (GND)  | GND           |

#### Controlador 1 (Dirección 16) - Ruedas Delanteras:
| Motoron | Motor Delantero Izq | Motor Delantero Der |
|---------|---------------------|---------------------|
| M1A+    | Motor+              | -                   |
| M1A-    | Motor-              | -                   |
| M1B+    | -                   | Motor+              |
| M1B-    | -                   | Motor-              |

#### Controlador 2 (Dirección 17) - Ruedas Traseras:
| Motoron | Motor Trasero Izq | Motor Trasero Der |
|---------|-------------------|-------------------|
| M1A+    | Motor+            | -                 |
| M1A-    | Motor-            | -                 |
| M1B+    | -                 | Motor+            |
| M1B-    | -                 | Motor-            |

#### Alimentación:
- **Raspberry Pi**: Fuente USB-C 5V/3A
- **Motores**: Fuente externa 220V AC a DC (1.8-22V) conectada a los controladores Motoron
  - Como se observa en la imagen del proyecto, se utiliza un adaptador de pared 220V AC que convierte a voltaje DC
  - La fuente se conecta directamente a los terminales de alimentación de los controladores Motoron
  - Verificar que el voltaje de salida sea compatible con los motores JGB37-520 (típicamente 6-12V)
- **GND común**: Conectar tierra de Raspberry Pi con controladores para referencia común

## 🧪 Pruebas

### Código de Prueba Básico
```python
#!/usr/bin/env python3

from motoron import MotoronI2C
import time

# Inicializar controladores
mc1 = MotoronI2C(address=16, bus=1)  # Ruedas delanteras
mc2 = MotoronI2C(address=17, bus=1)  # Ruedas traseras

try:
    # Reiniciar controladores
    mc1.reinitialize()
    mc2.reinitialize()
    
    # Habilitar motores
    mc1.clear_reset_flag()
    mc2.clear_reset_flag()
    
    print("Prueba de motores iniciada...")
    
    # Mover hacia adelante
    print("Adelante...")
    mc1.set_speed(1, 100)  # Motor delantero izquierdo
    mc1.set_speed(2, 100)  # Motor delantero derecho
    mc2.set_speed(1, 100)  # Motor trasero izquierdo
    mc2.set_speed(2, 100)  # Motor trasero derecho
    time.sleep(2)
    
    # Detener
    print("Deteniendo...")
    mc1.set_speed(1, 0)
    mc1.set_speed(2, 0)
    mc2.set_speed(1, 0)
    mc2.set_speed(2, 0)
    
    print("Prueba completada exitosamente!")
    
except Exception as e:
    print(f"Error durante la prueba: {e}")
```

### Ejecutar Prueba
```bash
# Guardar el código como test_motors.py
python3 test_motors.py
```

## 🔧 Troubleshooting

### Problemas Comunes

#### No se detectan controladores I2C
```bash
# Verificar que I2C esté habilitado
sudo raspi-config

# Verificar conexiones físicas
sudo i2cdetect -y 1

# Revisar cables SDA, SCL y GND
```

#### Los motores no responden
- Verificar alimentación externa a los controladores
- Comprobar que las direcciones I2C sean correctas
- Revisar conexiones Motor+ y Motor-

#### Error de permisos
```bash
# Agregar usuario al grupo i2c
sudo usermod -a -G i2c $USER

# Reiniciar sesión
```

#### Conflictos de librería
```bash
# Reinstalar librería Motoron
cd motoron-python
sudo python3 setup.py install --force
```

## 📝 Notas Adicionales

- **Voltaje de motores**: Los JGB37-520 operan típicamente entre 6-12V
- **Fuente de alimentación**: Se utiliza un adaptador 220V AC a DC como se muestra en las imágenes del proyecto
  - Asegurar que la fuente tenga suficiente corriente para los 4 motores
  - Verificar polaridad antes de conectar (+ y -)
- **Corriente máxima**: Verificar especificaciones del controlador Motoron
- **Encoders**: Si usas los encoders, conectar las señales A/B a pines GPIO adicionales
- **Protección**: Considera fusibles en la alimentación de motores

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**⚠️ Advertencia**: Siempre desconectar la alimentación antes de realizar cambios en las conexiones. Verificar polaridades antes de conectar los motores.
