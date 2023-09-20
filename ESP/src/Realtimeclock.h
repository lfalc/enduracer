#ifndef TIMEFUNCTIONS_H
#define TIMEFUNCTIONS_H
#include <Arduino.h>
#include <HTTPClient.h>
#include <TimeLib.h>
#include <WiFi.h>

const char *serverName = "192.168.1.101";
const int serverPort = 5000;

const unsigned long updateInterval = 60000; // Zeitintervall für die Aktualisierung der Uhrzeit in Millisekunden

unsigned long previousUpdateTime = 0;

long currenttime;

void processTime(String timeString) {
  // Hier kannst du den empfangenen Zeitstempel verarbeiten
  // und die interne Uhrzeit entsprechend setzen
  // Beispiel:
  long timestamp = timeString.toInt();
  setTime(timestamp);
}

bool getTimeFromServer() {
  HTTPClient http;
  
  // Baue die URL für die Zeitabfrage auf
  String url = "http://" + String(serverName) + ":" + String(serverPort) + "/time";
  
  http.begin(url);
  int httpCode = http.GET();
  
  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    Serial.println("Antwort vom Server: " + response);
    processTime(response);
    return true;
  }
  
  return false;
}

long getCurrentTimestamp() {
  // Gib den aktuellen Zeitstempel in Sekunden zurück
  return now();
}

void incrementTime() {
  // Erhöhe die interne Uhrzeit des ESP32 um eine Sekunde
  // Du kannst diese Funktion entsprechend anpassen, um die Zeit in anderen Einheiten zu erhöhen (z.B. Minuten, Stunden usw.)
  setTime(now() + 1);
}


#endif