# Como ejecutar el proyecto:

```python
python manage.py runserver IP_DE_TU_MAQUINA:8000
```

# Esquema de conexión:

### LEDs (Salidas):

- Conecta el ánodo (+) de cada LED a un pin GPIO del ESP32 (GPIO 23, 22, 21, 19).
- Conecta el cátodo (-) de cada LED a una resistencia de 220Ω, y esta a GND.

### Botones (Entradas):

- Conecta un extremo de cada botón a 3.3V del ESP32.
- Conecta el otro extremo a un pin GPIO (GPIO 18, 5, 17, 16) y a una resistencia de 1KΩ hacia GND.

# Codigo ESP32:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuración WiFi y servidor
const char* ssid = "Fam  Cazares Valenzuela";
const char* password = "Gera4628";
const char* serverURL = "http://192.168.0.106:8000/api/boton/"; // Cambia esto por la URL de tu servidor Django (IP DE TU PC)

// Configuración de pines
const int leds[] = {23, 22, 21, 19};    // Pines de LEDs (GPIO 23, 22, 21, 19)
const int botones[] = {18, 5, 17, 16};  // Pines de botones (GPIO 18, 5, 17, 16)

// Variables de estado y debounce
int paso_actual = 1;
bool error = false;
unsigned long ultimaPulsacion = 0; // Control de debounce

void setup() {
  Serial.begin(115200);
  conectarWiFi();

  // Configurar pines
  for (int i = 0; i < 4; i++) {
    pinMode(leds[i], OUTPUT);          // LEDs como salida
    pinMode(botones[i], INPUT_PULLUP); // Botones con pull-up interno
    digitalWrite(leds[i], LOW);        // Apagar todos los LEDs al inicio
  }

  // Encender LED del primer paso
  digitalWrite(leds[0], HIGH);
}

void loop() {
  // Verificar conexión WiFi
  if (WiFi.status() != WL_CONNECTED) {
    reconectarWiFi();
  }

  for (int i = 0; i < 4; i++) {
    if (digitalRead(botones[i]) == LOW && (millis() - ultimaPulsacion > 300)) { // Debounce de 300ms
      ultimaPulsacion = millis();
      enviarEventoBoton(i + 1);
      obtenerEstadoActual();
      actualizarLEDs();
    }
  }

  // Reconexión WiFi si es necesario
  if (WiFi.status() != WL_CONNECTED) reconectarWiFi();
}

// ========== FUNCIONES AUXILIARES ==========
void conectarWiFi() {
  Serial.println("\nConectando a WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado! IP: ");
  Serial.println(WiFi.localIP());
}

void enviarEventoBoton(int boton) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"boton\": " + String(boton) + "}";
    int httpCode = http.POST(payload);

    if (httpCode == HTTP_CODE_OK) {
      String respuesta = http.getString();
      Serial.println("Evento enviado: Botón " + String(boton));
    } else {
      Serial.println("Error en HTTP: " + String(httpCode));
    }

    http.end();
  }
}

void obtenerEstadoActual() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);

    int httpCode = http.GET();
    if (httpCode == HTTP_CODE_OK) {
      String respuesta = http.getString();
      DynamicJsonDocument doc(128);
      deserializeJson(doc, respuesta);

      paso_actual = doc["paso_actual"];
      error = doc["error"];

      Serial.println("Paso actual: " + String(paso_actual));
    }

    http.end();
  }
}

void actualizarLEDs() {
  // Apagar todos los LEDs
  for (int i = 0; i < 4; i++) {
    digitalWrite(leds[i], LOW);
  }

  // Encender solo el LED del paso actual (si está en rango)
  if (paso_actual >= 1 && paso_actual <= 4) {
    digitalWrite(leds[paso_actual - 1], HIGH);
  }

  // Parpadear si hay error
  if (error) {
    for (int i = 0; i < 3; i++) {
      digitalWrite(leds[paso_actual - 1], HIGH);
      delay(200);
      digitalWrite(leds[paso_actual - 1], LOW);
      delay(200);
    }
  }
}

void reconectarWiFi() {
  Serial.println("Reconectando WiFi...");
  WiFi.reconnect();
  delay(5000);
}
```
