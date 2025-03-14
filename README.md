# Robot Seguidor de Objetos con Visión Artificial

Robot autónomo para seguimiento de objetivos mediante detección de color, implementado con Arduino Mega y cámara Pixy2.

---

### Componentes Principales
- **Unidad de control**: Arduino Mega 2560
- **Sistema de visión**: Cámara Pixy2 CMUcam5
- **2 Motorreductores amarillos más ruedas**
- **Alimentación**: 2 baterías Li-ion 18650 (4.2V c/u)
- **Estructura**: Chasis con rueda loca multidireccional

---

## Proceso de Armado

### 1. Ensamblaje Mecánico
1. **Montaje de motores**:
   - Fijar motorreductores en laterales del chasis
   - Acoplar ruedas neumáticas a ejes motrices
   - Instalar rueda loca en parte frontal/trasera

2. **Integración de componentes**:
   - Fijar Arduino Mega en el chasis
   - Montar puente H cerca de los motores
   - Instalar Pixy2 en posición frontal
   - Asegurar porta pilas debajo del chasís

### 2. Conexiones Eléctricas
| Componente      | Pines Arduino | Alimentación |
|-----------------|---------------|--------------|
| Motor Izquierdo | 8 (IN1), 9 (IN2) | Puente H    |
| Motor Derecho   | 10 (IN3), 11 (IN4) | Puente H    |
| Pixy2           | SDA (20), SCL (21) | 5V Arduino |
| Puente H        | -             | Baterías (7-12V) |
| Arduino Mega    | -             | Baterías (7-9V)  |


---

## Arquitectura del Sistema

### 1. Módulo de Percepción
- **Pixy2**: Configurada para detectar objetos con signature 1

### 2. Lógica de Control
- **Dualidad operacional**:
  - **Fase de búsqueda**: Rotación sobre eje hasta detección inicial
  - **Fase de seguimiento**: Control PID para mantenimiento de posición

- **Parámetros PID**:
  - Proporcional (Kp): 0.2
  - Integral (Ki): 0.01 
  - Derivativo (Kd): 0.1
  - Frecuencia de actualización: ~200Hz

### 3. Sistema de Movimiento
- **Configuración diferencial**: Control independiente de motores
- **Rango PWM**: 0-120 (óptimo para reducción de deslizamiento)
- **Protocolo de seguridad**: Detención automática ante proximidad crítica (ancho objetivo >150px)

---

## Implementación

### Diagrama de Conexiones
| Componente      | Pines Arduino | Notas               |
|-----------------|---------------|---------------------|
| Motor Izquierdo | 8 (IN1), 9 (IN2) | Configuración PWM |
| Motor Derecho   | 10 (IN3), 11 (IN4) | Configuración PWM |
| Pixy2           | SDA (20), SCL (21) | Protocolo I2C    |

### Flujo de Operación
1. Inicialización de periféricos (motores, cámara)
2. Bucle principal:
   - Captura de datos de la cámara
   - Cálculo de posición relativa del objetivo
   - Aplicación de algoritmo PID para corrección de trayectoria
   - Activación/desactivación de motores según modo operativo
   - Verificación constante de condiciones de seguridad

---

## Personalización Avanzada

1. **Calibración Visual**:
   - Ajustar `CENTER_X` según montaje físico de la cámara
   - Modificar `MIN_DISTANCIA` en función de distancia operativa deseada

2. **Parámetros Dinámicos**:
   ```cpp
   // Control de velocidad base
   int baseSpeed = 100;  // Rango recomendado: 80-150
   
   // Factores de respuesta
   float Kp = 0.2;  // Incrementar para mayor reactividad
   float Ki = 0.01; // Reducir para disminuir oscilaciones
