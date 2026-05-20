#include <Arduino.h>
#include <WiFi.h>
#include <ESP32Servo.h>
#include <PubSubClient.h>
#include "secrets.h"

// --- CONFIGURACIÓN WI-FI ---
const int wifiRetryAttempts = 20;

// --- CONFIGURACIÓN HARDWARE ---
Servo miServo; 
const int pinServo = 18;

// --- OBJETOS ---
WiFiClient espClient;
PubSubClient client(espClient);

// Declaración de funciones
void conectarWiFi();
void dispensarComida();
void conectarMQTT();
void callback(char* topic, byte* payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    delay(10);

    conectarWiFi();

    // Configurar servidor MQTT y función de escucha (callback)
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
    
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    miServo.setPeriodHertz(50);
    miServo.attach(pinServo, 500, 2400);
    miServo.write(0); // Asegurar posición cerrado al arrancar
    Serial.println("\n[SISTEMA] Todo listo y compuerta cerrada.");
}

void loop() {
    // Si por alguna razón se desconecta del Wi-Fi, intenta reconectar automáticamente
    if (WiFi.status() != WL_CONNECTED) {
        conectarWiFi();
    }

    if (!client.connected()) {
        conectarMQTT();
    }
    
    // Esta función mantiene viva la comunicación MQTT y procesa mensajes entrantes
    client.loop();
    delay(10);
}

void conectarWiFi() {
    Serial.println();
    Serial.print("[WI-FI] Conectando a ");
    Serial.println(ssid);

    // Iniciar el módulo Wi-Fi en modo estación (cliente)
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    // Esperar a que se conecte
    int intentos = 0;
    while (WiFi.status() != WL_CONNECTED && intentos < wifiRetryAttempts) {
        delay(500);
        Serial.print(".");
        intentos++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("");
        Serial.println("[WI-FI] ¡Conectado con éxito!");
        Serial.print("[WI-FI] Dirección IP asignada: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("");
        Serial.println("[WI-FI] Error: No se pudo conectar. Reintentando en el siguiente ciclo...");
    }
}

void dispensarComida() {
    int posicionCerrado = 0;
    int posicionAbierto = 90;

    Serial.println("\n[MOTOR] Dispensando comida... Girando al agujero.");
    miServo.write(posicionAbierto);
    
    delay(1200); // Tiempo de caída de croquetas
    
    Serial.println("[MOTOR] Cerrando compuerta. Regresando a posición original.");
    miServo.write(posicionCerrado);
}

void conectarMQTT() {
    while (!client.connected()) {
        Serial.print("[MQTT] Intentando conexión al broker...");
        // Creamos un ID de cliente único basado en el tiempo
        char* clientId = "FeederDevice";
        
        if (client.connect(clientId, mqtt_user, mqtt_pass)) {
            Serial.println(" ¡Conectado!");
            // Nos suscribimos al tópico para escuchar órdenes
            client.subscribe(topic_sub);
            Serial.print("[MQTT] Suscrito al tópico: ");
            Serial.println(topic_sub);
        } else {
            Serial.print(" Falló, rc=");
            Serial.print(client.state());
            Serial.println(" Reintentando en 5 segundos...");
            delay(5000);
        }
    }
}

// Esta función se ejecuta automáticamente cuando llega un mensaje MQTT
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("\n[MQTT] Mensaje recibido en [");
    Serial.print(topic);
    Serial.print("]: ");
    
    String mensaje = "";
    for (int i = 0; i < length; i++) {
        mensaje += (char)payload[i];
    }
    Serial.println(mensaje);

    // Si recibimos un "1", se activa el dispensador
    if (mensaje == "1") {
        dispensarComida();
    }
}