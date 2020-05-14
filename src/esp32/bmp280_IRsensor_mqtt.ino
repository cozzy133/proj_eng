/*
 * Author : Padraig O Cosgora
 * BMP280, IR Sensor
 * MQTT connection
 */

/***************************************************************************
  This is a library for the BMP280 humidity, temperature & pressure sensor

  Designed specifically to work with the Adafruit BMP280 Breakout
  ----> http://www.adafruit.com/products/2651

  These sensors use I2C or SPI to communicate, 2 or 4 pins are required
  to interface.

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Limor Fried & Kevin Townsend for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <WiFi.h>
#include <PubSubClient.h>

int isObstaclePin = 2; // This is our input pin
int isObstacle = HIGH; // HIGH MEANS NO OBSTACLE
Adafruit_BMP280 bmp; // I2C

const char* ssid = "VM5E1BF2F"; // Enter your WiFi name
const char* password =  "Gr091443588!"; // Enter WiFi password
const char* mqttServer = "hairdresser.cloudmqtt.com";
const int mqttPort = 17043;
const char* mqttUser = "cmszpdkk";
const char* mqttPassword = "Z0_OVJO9x11Z";
#define MQTT_SERIAL_PUBLISH_TEMP "/fyp/temp"
#define MQTT_SERIAL_PUBLISH_PRESSURE "/fyp/pressure"
#define MQTT_SERIAL_PUBLISH_ALTITUDE "/fyp/altitude"
#define MQTT_SERIAL_PUBLISH_OBSTACLE "/fyp/obstacle"
#define MQTT_SERIAL_RECEIVER_CH "/fyp/subscribe"
char charVal[10]; 

WiFiClient wifiClient;

PubSubClient client(wifiClient);

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    randomSeed(micros());
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(),mqttUser,mqttPassword)) {
      Serial.println("connected");
      //Once connected, publish an announcement...
      client.publish("/fyp/connection", "hello world");
      // ... and resubscribe
      client.subscribe(MQTT_SERIAL_RECEIVER_CH);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
    Serial.println("-------new message from broker-----");
    Serial.print("channel:");
    Serial.println(topic);
    Serial.print("data:"); 
    Serial.write(payload, length);
    Serial.println();
}

void publishData(char *serialData, char *topic){
  if (!client.connected()) {
    reconnect();
  }
  client.publish(topic, serialData);
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);// Set time out for 
  setup_wifi();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  reconnect();
  Serial.println(F("BMP280 test"));

  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }
  pinMode(isObstaclePin, INPUT); // then we have the out pin from the module

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
    client.loop();
    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");

    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");

    Serial.print(F("Approx altitude = "));
    Serial.print(bmp.readAltitude(1029.25)); 
    Serial.println(" m");
    isObstacle = digitalRead(isObstaclePin);
    float vIn4 = 0;
    if (isObstacle == LOW) {
        Serial.println("OBSTACLE!!, OBSTACLE!!");
        vIn4 = 1;
    } else {
        Serial.println("clear");
        vIn4 = 0;
    }
    Serial.println();
    float vIn = bmp.readTemperature();
    float vIn2 = bmp.readPressure();
    float vIn3 = bmp.readAltitude(1029.25);
    dtostrf(vIn, 4, 3, charVal);
    publishData(charVal, MQTT_SERIAL_PUBLISH_TEMP);
    dtostrf(vIn2, 4, 3, charVal);
    publishData(charVal, MQTT_SERIAL_PUBLISH_PRESSURE);
    dtostrf(vIn3, 4, 3, charVal);
    publishData(charVal, MQTT_SERIAL_PUBLISH_ALTITUDE);
    dtostrf(vIn4, 4, 3, charVal);
    publishData(charVal, MQTT_SERIAL_PUBLISH_OBSTACLE);
    delay(2000);
}
