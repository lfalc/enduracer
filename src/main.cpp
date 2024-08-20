using namespace std;
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include "FS.h"
#include "Realtimeclock.h"

// Replace with your network credentials
const char *ssid1 = "FRITZ!Box 7590 GE";
const char *password1 = "46873571718242819466";

const char *ssid = "EnduroRace";
const char *password = "EnduroRace";

const char *ssid2 = "HUAWEI-E5776-3FC7";
const char *password2 = "2B2TABT9G3Q";

WiFiClient client;

// Set RFID reader pins
#define RST_PIN 22
#define SS_PIN 21
// Set LED pins
#define White 32
#define White2 33
#define Red_Led 25

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.

// Set initial name
String name = "Unknown";
String previousUid = "";

//--------------------------------------------------------------------------------------------------


void connectToWiFi()
{
  // WiFi.mode(WIFI_STA);
  Serial.println("Connecting to Wi-Fi 1");
  WiFi.begin(ssid, password);
  int x = 0;
  int y = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    if (x < 10)
    {
      Serial.println("Connecting to WiFi...");
      delay(1000);
      x++;
    }
    else
    {
      Serial.println("Connecting to WiFi 2");
      WiFi.begin(ssid1, password1);
      while (WiFi.status() != WL_CONNECTED)
      {
        if (y < 10)
        {

          Serial.println("Connecting to WiFi...");
          delay(1000);
          y++;
        }
        else
        {
          Serial.println("Connecting to WiFi 3");
          WiFi.begin(ssid2, password2);

          while (WiFi.status() != WL_CONNECTED)
          {
            {
              Serial.println("Connecting to WiFi...");
              delay(1000);
            }
          }
        }
      }
    }
  }
  Serial.println("Connected to Wi-Fi");
  Serial.println(WiFi.localIP());
}

void postRequest(String name)
{
  WiFiClient client;
  if (!client.connect(serverName, serverPort))
  {
    Serial.println("Connection failed");
    digitalWrite(Red_Led, HIGH);
    delay(1000);
    return;
  }
  digitalWrite(Red_Led, LOW);


  String url = "/receive";

  DynamicJsonDocument data(1024);
  data["name"] = name;
  data["timestamp"] = currenttime;
  String json;
  serializeJson(data, json);

  Serial.println("Making HTTP POST request");
  client.println("POST " + url + " HTTP/1.1");
  client.println("Host: " + String(serverName));
  client.println("Content-Type: application/json");
  client.println("Content-Length: " + String(json.length()));
  client.println();
  client.print(json);

  // delay(500);

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

  if (getTimeFromServer())
  {
    // Zeit erfolgreich empfangen und verarbeitet
    // Setze die interne Uhrzeit des ESP32 entsprechend
    setTime(getCurrentTimestamp());
    Serial.println("Erfasste Zeit: " + String(getCurrentTimestamp()));
  }
  else
  {
    // Fehler beim Empfangen der Zeit
    Serial.println("Fehler beim Empfangen der Zeit");
  }

  pinMode(White, OUTPUT);
  pinMode(White2, OUTPUT);
  pinMode(Red_Led, OUTPUT);
}

void loop()
{ // Check if RFID tag is detected
  currenttime = getCurrentTimestamp();
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
        if (buffer2[i] != 30)
        {
          Nachname += (char)buffer2[i];
        }
      }
      //------------------------------------------------------------------------------------------
      // Only for Serial Output
      // PRINT FIRST NAME
      for (uint8_t i = 0; i < 16; i++)
      {
        if (buffer1[i] != 32)
        {
          Serial.write(buffer1[i]);
        }
      }
      Serial.print(" ");

      // PRINT LAST NAME
      for (uint8_t i = 0; i < 16; i++)
      {
        if (buffer2[i] != 30)
        {
          Serial.write(buffer2[i]);
        }
      }
      Serial.print(',');

      //------------------------------------------------------------------------------------------

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
