import time
import motoron
import RPi.GPIO as GPIO
import threading
from collections import deque
import atexit
import sys
import tty
import termios
import select

# Configuracin de GPIO
try:
    GPIO.cleanup()
except:
    pass

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definicin de pines de encoders
ENCODER_PINS = {
    'mc1_motor2': {'pin_a': 4, 'pin_b': 10, 'name': 'abajo_izquierda'},
    'mc1_motor3': {'pin_a': 18, 'pin_b': 17, 'name': 'arriba_izquierda'},
    'mc2_motor1': {'pin_a': 22, 'pin_b': 27, 'name': 'abajo_derecha'},
    'mc2_motor2': {'pin_a': 23, 'pin_b': 4, 'name': 'arriba_derecha'}
}

# Variables globales para control
motor_speeds = {
    'abajo_izquierda': 0,
    'arriba_izquierda': 0,
    'abajo_derecha': 0,
    'arriba_derecha': 0
}

# Velocidades de operacin
BASE_SPEED = 400
TURN_SPEED = 300

class EncoderReader:
    def __init__(self, pin_a, pin_b, name, pulses_per_revolution=720):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.name = name
        self.pulses_per_revolution = pulses_per_revolution
        
        self.position = 0
        self.last_position = 0
        self.last_time = time.time()
        
        self.velocity_samples = deque(maxlen=5)
        self.current_velocity = 0.0
        
        self.last_a = 0
        self.last_b = 0
        
        self.total_pulses_detected = 0
        self.last_activity_time = time.time()
        self.activity_detected = False
        
        try:
            GPIO.remove_event_detect(self.pin_a)
            GPIO.remove_event_detect(self.pin_b)
        except:
            pass
        
        # Configurar pines
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        time.sleep(0.1)
        
        # Leer estado inicial
        self.last_a = GPIO.input(self.pin_a)
        self.last_b = GPIO.input(self.pin_b)
        
        print(f"Encoder {self.name} inicializado - Estado inicial A:{self.last_a}, B:{self.last_b}")
    
    def read_encoder_state(self):
        """Lee el estado actual de los pines del encoder"""
        return GPIO.input(self.pin_a), GPIO.input(self.pin_b)
    
    def update_encoder_reading(self):
        """Actualizar lectura por polling"""
        current_a, current_b = self.read_encoder_state()
        
        if current_a != self.last_a or current_b != self.last_b:
            self.activity_detected = True
            self.last_activity_time = time.time()
            
            if current_a != self.last_a:
                if current_a == current_b:
                    self.position += 1
                else:
                    self.position -= 1
                self.total_pulses_detected += 1
            elif current_b != self.last_b:
                if current_a != current_b:
                    self.position += 1
                else:
                    self.position -= 1
                self.total_pulses_detected += 1
            
            self.last_a = current_a
            self.last_b = current_b
    
    def calculate_velocity(self):
        """Calcula la velocidad en RPM"""
        self.update_encoder_reading()
        
        current_time = time.time()
        time_diff = current_time - self.last_time
        
        if time_diff >= 0.1:
            position_diff = self.position - self.last_position
            
            rpm = (position_diff / time_diff) * 60.0 / self.pulses_per_revolution
            
            self.velocity_samples.append(rpm)
            self.current_velocity = sum(self.velocity_samples) / len(self.velocity_samples)
            
            self.last_position = self.position
            self.last_time = current_time
        
        return self.current_velocity
    
    def get_diagnostic_info(self):
        """Retorna informacin de diagnstico"""
        current_time = time.time()
        time_since_activity = current_time - self.last_activity_time
        
        return {
            'position': self.position,
            'velocity': self.current_velocity,
            'total_pulses': self.total_pulses_detected,
            'time_since_activity': time_since_activity,
            'is_active': time_since_activity < 1.0,
            'pin_states': self.read_encoder_state()
        }
        
# Crear objetos de encoders
encoders = {}
for motor_id, config in ENCODER_PINS.items():
    encoders[motor_id] = EncoderReader(
        config['pin_a'], 
        config['pin_b'], 
        config['name']
    )

# Crear objetos Motoron con las direcciones establecidas en los drivers pololu
mc1 = motoron.MotoronI2C(address=16)
mc2 = motoron.MotoronI2C(address=17)

def setup_motoron(mc):
    mc.reinitialize()
    mc.disable_crc()
    mc.clear_reset_flag()
    mc.set_command_timeout_milliseconds(50000)

setup_motoron(mc1)
setup_motoron(mc2)

# Configurar aceleracin y desaceleracin ms suaves
mc1.set_max_acceleration(2, 40)
mc1.set_max_deceleration(2, 100)
mc1.set_max_acceleration(3, 40)
mc1.set_max_deceleration(3, 100)
mc2.set_max_acceleration(1, 40)
mc2.set_max_deceleration(1, 100)
mc2.set_max_acceleration(2, 40)
mc2.set_max_deceleration(2, 100)

def update_motor_speeds():
    """Actualiza las velocidades de los motores basado en motor_speeds"""
    mc1.set_speed(2, motor_speeds['abajo_izquierda'])
    mc1.set_speed(3, motor_speeds['arriba_izquierda'])
    mc2.set_speed(1, motor_speeds['abajo_derecha'])
    mc2.set_speed(2, motor_speeds['arriba_derecha'])

def move_forward():
    """Mover hacia adelante"""
    motor_speeds['abajo_izquierda'] = BASE_SPEED
    motor_speeds['arriba_izquierda'] = BASE_SPEED
    motor_speeds['abajo_derecha'] = BASE_SPEED
    motor_speeds['arriba_derecha'] = BASE_SPEED
    update_motor_speeds()

def move_backward():
    """Mover hacia atr"""
    motor_speeds['abajo_izquierda'] = -BASE_SPEED
    motor_speeds['arriba_izquierda'] = -BASE_SPEED
    motor_speeds['abajo_derecha'] = -BASE_SPEED
    motor_speeds['arriba_derecha'] = -BASE_SPEED
    update_motor_speeds()

def turn_left():
    """Girar a la izquierda"""
    motor_speeds['abajo_izquierda'] = -TURN_SPEED
    motor_speeds['arriba_izquierda'] = -TURN_SPEED
    motor_speeds['abajo_derecha'] = TURN_SPEED
    motor_speeds['arriba_derecha'] = TURN_SPEED
    update_motor_speeds()

def turn_right():
    """Girar a la derecha"""
    motor_speeds['abajo_izquierda'] = TURN_SPEED
    motor_speeds['arriba_izquierda'] = TURN_SPEED
    motor_speeds['abajo_derecha'] = -TURN_SPEED
    motor_speeds['arriba_derecha'] = -TURN_SPEED
    update_motor_speeds()

def stop_motors():
    """Detener todos los motores"""
    motor_speeds['abajo_izquierda'] = 0
    motor_speeds['arriba_izquierda'] = 0
    motor_speeds['abajo_derecha'] = 0
    motor_speeds['arriba_derecha'] = 0
    update_motor_speeds()
    
def print_diagnostic_report():
    """Funcin para mostrar diagnstico completo"""
    print("\n" + "="*100)
    print(f"{'Motor':<20} {'Pos':<8} {'RPM':<8} {'Pulsos':<8} {'Activo':<8} {'PinA':<6} {'PinB':<6} {'Estado':<15}")
    print("-"*100)
    
    for motor_id, encoder in encoders.items():
        diag = encoder.get_diagnostic_info()
        
        # Determinar estado del motor
        if diag['total_pulses'] == 0:
            status = "SIN_SEAL"
        elif not diag['is_active']:
            status = "INACTIVO"
        elif abs(diag['velocity']) < 0.5:
            status = "MUY_LENTO"
        else:
            status = "OK"
        
        print(f"{encoder.name:<20} {diag['position']:<8} {diag['velocity']:<8.2f} "
              f"{diag['total_pulses']:<8} {diag['is_active']:<8} "
              f"{diag['pin_states'][0]:<6} {diag['pin_states'][1]:<6} {status:<15}")
    
    # Mostrar velocidades actuales de motores
    print(f"\nVelocidades actuales:")
    print(f"Izq: {motor_speeds['abajo_izquierda']:>4}/{motor_speeds['arriba_izquierda']:>4} | "
          f"Der: {motor_speeds['abajo_derecha']:>4}/{motor_speeds['arriba_derecha']:>4}")
    print("="*100)

def velocity_monitoring_thread():
    """Hilo para monitoreo continuo"""
    while True:
        for encoder in encoders.values():
            encoder.calculate_velocity()
        time.sleep(0.01)
        
def keyboard_input_thread():
    """Hilo para capturar entrada de teclado sin bloquear"""
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    
    try:
        while True:
            if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                key = sys.stdin.read(1).lower()
                
                if key == 'w':
                    print("?? ADELANTE")
                    move_forward()
                elif key == 's':
                    print("?? ATRS")
                    move_backward()
                elif key == 'a':
                    print("?? IZQUIERDA")
                    turn_left()
                elif key == 'd':
                    print("?? DERECHA")
                    turn_right()
                elif key == ' ':  # Espacio para parar
                    print("?? STOP")
                    stop_motors()
                elif key == 'q':
                    print("?? SALIENDO...")
                    stop_motors()
                    break
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def cleanup_gpio():
    print("Limpiando configuracin GPIO...")
    stop_motors()
    GPIO.cleanup()

atexit.register(cleanup_gpio)

# Iniciar hilos
velocity_thread = threading.Thread(target=velocity_monitoring_thread, daemon=True)
velocity_thread.start()

keyboard_thread = threading.Thread(target=keyboard_input_thread, daemon=True)
keyboard_thread.start()

try:
    print("\n" + "="*60)
    print("?? CONTROL DE MOTORES CON TECLADO")
    print("="*60)
    print("CONTROLES:")
    print("  W - Avanzar")
    print("  S - Retroceder") 
    print("  A - Girar izquierda")
    print("  D - Girar derecha")
    print("  ESPACIO - Parar")
    print("  Q - Salir")
    print("="*60)
    print("Los motores estn listos. Usa las teclas para controlar.")
    print("Presiona Q para salir del programa")
    print("="*60)
    
    # Bucle principal - mostrar datos cada 2 segundos
    while keyboard_thread.is_alive():
        print_diagnostic_report()
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n?? Programa interrumpido...")
    
finally:
    print("?? Deteniendo motores...")
    stop_motors()
    time.sleep(0.5)
    GPIO.cleanup()
    print("? GPIO limpiado y programa terminado")
