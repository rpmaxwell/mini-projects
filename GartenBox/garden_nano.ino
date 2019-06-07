#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <dht.h>

SoftwareSerial esp(10, 11); // RX, TX

dht DHT;
#define DHT11_PIN 6
#define PHOTOCELL_PIN 0
#define LAMP_PIN 5
#define SOIL_SENSOR 2


void setup() {
  Serial.begin(9600);
  while (!Serial) {
    Serial.print(".");
  }
  Serial.println("nano setup finished.");
  esp.begin(9600);
  pinMode(LAMP_PIN, OUTPUT);
  pinMode(SOIL_SENSOR, INPUT);
  digitalWrite(LAMP_PIN, HIGH);
}

void loop() {
  while (Serial.available() > 0) {
    esp.write(Serial.read());
  }
  while (esp.available() > 0) {
    Serial.write(esp.read());
    Serial.flush();
    delay(10);
  }
  int chk = DHT.read11(DHT11_PIN);
  float temp = DHT.temperature;
  esp.println("<1,1," + String(temp)+">");
//  digitalWrite(LAMP_PIN, LOW);
  delay(1000);
  float humidity = DHT.humidity;
  esp.println("<1,2," + String(humidity)+">");
//  delay(1000);
//  digitalWrite(LAMP_PIN, HIGH);
  int photocellReading = analogRead(PHOTOCELL_PIN);
  esp.println("<2,3," + String(photocellReading) + ">");
  delay(1000);
  int soilReading = analogRead(SOIL_SENSOR);
  esp.println("<3,4," + String(soilReading) + ">");
 delay(10000);
}
