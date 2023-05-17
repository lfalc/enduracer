using namespace std;
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
//#include <WebServer.h>
//#include <HTTPClient.h>
//#include <esp_http_client.h>
#include <ArduinoJson.h>
//#include <WiFiUdp.h>
//#include <NTPClient.h>
#include <time.h>
#include "FS.h"

// Replace with your network credentials
const char *ssid = "FRITZ!Box 7590 GE";
const char *password = "46873571718242819466";

// const char *ssid = "Obi Wlan Kenobi";
// const char *password = "Biergewitter";

// Fixed IP data:
/*const IPAddress ip(192, 168, 178, 110);
const IPAddress gateway(192, 168, 178, 1);
const IPAddress subnet(255, 255, 255, 0);*/
const char *serverName = "192.168.178.125";

WiFiClient client;

// Set RFID reader pins
#define RST_PIN 22
#define SS_PIN 21
// Set LED pins
#define White 32
#define White2 33

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.

// Set initial name
String name = "Unknown";
String previousUid = "";

// NTP server to request epoch time
const char *ntpServer = "fritz.box";

// Variable to save current epoch time
unsigned long epochTime;

// Function that gets current epoch time
unsigned long getTime()
{
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    // Serial.println("Failed to obtain time");
    return (0);
  }
  time(&now);
  return now;
}

void connectToWiFi()
{
  //WiFi.mode(WIFI_STA);
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to Wi-Fi");
  Serial.println(WiFi.localIP());
}

void postRequest(String name)
{
  WiFiClient client;

  if (!client.connect(serverName, 5000))
  {
    Serial.println("Connection failed");
    delay(1000);
    return;
  }

  String url = "/receive";

  DynamicJsonDocument data(1024);
  data["name"] = name;
  data["timestamp"] = epochTime;
  String json;
  serializeJson(data, json);

  Serial.println("Making HTTP POST request");
  client.println("POST " + url + " HTTP/1.1");
  client.println("Host: " + String(serverName));
  client.println("Content-Type: application/json");
  client.println("Content-Length: " + String(json.length()));
  client.println();
  client.print(json);

  //delay(500);

  while (client.available())
  {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }

  client.stop();
  Serial.println("\nHTTP POST request done");
  digitalWrite(White, HIGH);
  digitalWrite(White2, HIGH);
  delay(200); // change value if you want to read cards faster
}

void setup()
{
  Serial.begin(9600);
  // If you want fixed IP data uncomment the following line
  // WiFi.config(ip, gateway, subnet);
  connectToWiFi();

  // Initialize SPI bus
  SPI.begin();

  // Initialize MFRC522 RFID reader
  mfrc522.PCD_Init();

  configTime(0, 0, ntpServer);

  pinMode(White, OUTPUT);
  pinMode(White2, OUTPUT);

}

void loop()
{
  epochTime = getTime();
  // Check if RFID tag is detected
  digitalWrite(White, LOW);
  digitalWrite(White2, LOW);
  String Vorname = "";
  String Nachname = "";

  // Prepare key - all keys are set to FFFFFFFFFFFFh at chip delivery from the factory.
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++)
    key.keyByte[i] = 0xFF;
  // some variables we need
  byte block;
  byte len;
  MFRC522::StatusCode status;

  //-------------------------------------------

  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial())
  {
    String uid = "";
    byte buffer1[18];

    block = 4;
    len = 18;

    //-----------------------------------------------------------
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }

    if (uid != previousUid)
    {

      //------------------------------------------- GET FIRST NAME
      status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid)); // line 834 of MFRC522.cpp file
      if (status != MFRC522::STATUS_OK)
      {
        Serial.print(F("Authentication failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));

        return;
      }

      status = mfrc522.MIFARE_Read(block, buffer1, &len);
      if (status != MFRC522::STATUS_OK)
      {
        Serial.print(F("Reading failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));

        mfrc522.PCD_Reset();
        mfrc522.PCD_Init();

        return;
      }

      //---------------------------------------- GET LAST NAME

      byte buffer2[18];
      block = 1;

      status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 1, &key, &(mfrc522.uid)); // line 834
      if (status != MFRC522::STATUS_OK)
      {
        Serial.print(F("Authentication failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
      }

      status = mfrc522.MIFARE_Read(block, buffer2, &len);
      if (status != MFRC522::STATUS_OK)
      {
        Serial.print(F("Reading failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));

        mfrc522.PCD_Reset();
        mfrc522.PCD_Init();
        return;
      }

      // STORE FIRST NAME
      for (uint8_t i = 0; i < 16; i++)
      {
        if (buffer1[i] != 32)
        {
          Vorname += (char)buffer1[i];
        }
      }

      // STORE LAST NAME
      for (uint8_t i = 0; i < 16; i++)
      {
        if (buffer1[i] != 30)
        {
          Nachname += (char)buffer2[i];
        }
      }

      name = Vorname + " " + Nachname;

      postRequest(name);

      previousUid = uid;
    }
    else
    {
      return;
    }

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
  }
}
