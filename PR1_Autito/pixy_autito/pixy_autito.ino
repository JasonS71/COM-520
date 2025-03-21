#include <Pixy2.h>

// Configuración de pines motores
int izq1 = 8;    // Adelante izquierdo
int izq2 = 9;    // Atrás izquierdo
int der1 = 10;   // Adelante derecho
int der2 = 11;   // Atrás derecho

// Parámetros de la cámara
#define CENTER_X 160      // Centro horizontal de la vista de Pixy2 (320px)
#define MIN_DISTANCIA 150 // Ancho mínimo del objeto para considerarlo cerca (ajustar)

// Parámetros del control PID
float Kp = 0.2;   // Ganancia proporcional
float Ki = 0.01;  // Ganancia integral
float Kd = 0.1;   // Ganancia derivativa

// Variables del sistema
Pixy2 pixy;
int errorAnterior = 0;
int integral = 0;
bool fase2 = false;

void setup() {
  Serial.begin(115200);
  
  // Configurar pines de motores como salidas
  pinMode(izq1, OUTPUT);
  pinMode(izq2, OUTPUT);
  pinMode(der1, OUTPUT);
  pinMode(der2, OUTPUT);
  
  pixy.init();
  // Iniciar en Fase 1
  girarEnPropioEje();
}

void loop() {
  pixy.ccc.getBlocks();
  
  if (fase2) {
    // Modo seguimiento
    if (pixy.ccc.numBlocks) {
      for (int i = 0; i < pixy.ccc.numBlocks; i++) {
        if (pixy.ccc.blocks[i].m_signature == 1) {
          int objetoX = pixy.ccc.blocks[i].m_x;
          int objetoWidth = pixy.ccc.blocks[i].m_width;
          
          // Condición de detención por proximidad
          if (objetoWidth >= MIN_DISTANCIA) {
            pararMotores();
            Serial.println("Objeto demasiado cerca - DETENIENDO");
            return; // Salir del loop temporalmente
          }
          
          // Calcular error
          int error = CENTER_X - (objetoX + objetoWidth/2);
          
          // Cálculos PID
          integral += error;
          int derivada = error - errorAnterior;
          int ajustePID = (Kp * error) + (Ki * integral) + (Kd * derivada);
          
          controlarMotores(ajustePID);
          
          errorAnterior = error;
          break;
        }
      }
    } else {
      // Si pierde el objeto, volver a Fase 1
      fase2 = false;
      girarEnPropioEje();
    }
  } else {
    // Fase 1: Búsqueda
    if (pixy.ccc.numBlocks) {
      for (int i = 0; i < pixy.ccc.numBlocks; i++) {
        if (pixy.ccc.blocks[i].m_signature == 1) {
          // Verificar distancia incluso en fase de búsqueda
          if (pixy.ccc.blocks[i].m_width >= MIN_DISTANCIA) {
            pararMotores();
            Serial.println("Objeto detectado cerca durante búsqueda - DETENIENDO");
            return;
          }
          
          // Detectar objeto, entrar en Fase 2
          fase2 = true;
          pararMotores();
          delay(100);  // Pequeña pausa antes de iniciar seguimiento
          break;
        }
      }
    }
  }
  delay(5);
}

// Resto de funciones permanecen igual (girarEnPropioEje, pararMotores, controlarMotores)

void girarEnPropioEje() {
  // Izquierda adelante, derecha atrás
  analogWrite(izq1, 80);
  analogWrite(izq2, 0);
  analogWrite(der1, 0);
  analogWrite(der2, 80);
}

void pararMotores() {
  analogWrite(izq1, 0);
  analogWrite(izq2, 0);
  analogWrite(der1, 0);
  analogWrite(der2, 0);
}

void controlarMotores(int ajuste) {
  // Ajuste positivo = objeto a la izquierda
  // Ajuste negativo = objeto a la derecha
  
  int baseSpeed = 100;  // Velocidad base máxima (160)
  int maxAjuste = 30;   // Reducido para mejor control
  
  // Calcular velocidades con límites
  int velocidadIzq = baseSpeed + constrain(ajuste, -maxAjuste, maxAjuste);
  int velocidadDer = baseSpeed - constrain(ajuste, -maxAjuste, maxAjuste);
  
  // Aplicar límite máximo de 160
  velocidadIzq = constrain(velocidadIzq, 0, 120);
  velocidadDer = constrain(velocidadDer, 0, 120);
  
  // Aplicar velocidades
  analogWrite(izq2, velocidadIzq);  // PWM en pin de dirección
  analogWrite(der1, velocidadDer);  // PWM en pin de dirección
  
  // Configurar dirección (ambos motores adelante)
  analogWrite(izq1, 100);
  analogWrite(izq2, 0);
  analogWrite(der1, 100);
  analogWrite(der2, 0);
  
  // (Opcional) Debug de velocidades
  Serial.print("Vel Izq: ");
  Serial.print(velocidadIzq);
  Serial.print(" | Vel Der: ");
  Serial.println(velocidadDer);
}
