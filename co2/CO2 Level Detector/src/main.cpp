#include "main.h"
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "Adafruit_CCS811.h"
#include <ArduinoJson.h>

WiFiClient client;
PubSubClient psClient(client);
Adafruit_CCS811 ccs;
StaticJsonDocument<100> alertDoc;

void setup()
{

  Serial.begin(115200);

  // Setup Wi-Fi
  Serial.printf("Connecting to %s network...\n", ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pwd);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.printf("Successfully connected to %s network...\n", ssid);

  // Initialize MQTT
  psClient.setServer(mqttBroker, mqttPort);
  if (psClient.connect(mqttClientId, mqttUsername, mqttPassword))
  {
    Serial.println("MQTT connected successfully!");
  }

  if (!ccs.begin())
  {
    Serial.println("Failed to start sensor! Please check your wiring.");
    while (1)
      ;
  }

  // Wait for the sensor to be ready
  while (!ccs.available())
    ;
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (ccs.available())
  {
    uint16_t co2 = ccs.geteCO2();

    // if CO2 levels are above 400ppm, send alert
    if (co2 > 400)
    {
      Serial.printf("CO2 Level is above 400 (%d), sending alert...", co2);

      alertDoc["message"] = "high_co2_level";
      alertDoc["level"] = co2;
      String alertMsg;
      serializeJson(alertDoc, alertMsg);

      bool sendAlert = psClient.publish(co2WarningTopic, alertMsg.c_str());
      if (sendAlert)
      {
        Serial.println("CO2 Level Alert Sent Successfully");
      }
      else
      {
        Serial.println("[WARNING] Failed to send CO2 Level Alert!");
      }
    }
  }
}