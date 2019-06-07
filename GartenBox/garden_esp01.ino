#include "ESP8266WiFi.h"
#include "ArduinoJson.h"
#include "ArduinoJson.h"
#include "ESP8266HTTPCli ent.h"

const char* ssid     = "SSID";
const char* password = "SSID_PASSWORD";

char JSONmessageBuffer[1024];
boolean newData;
const byte numChars = 10;
char receivedChars[numChars];
char tempChars[numChars];
int deviceId = 0;
int measurementId = 0;
float measurementValue = 0.0;


void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  delay(100);
  
  Serial.println("esp setup done");
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");             
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
}

void loop() {
  receiveData();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseData();
        newData = false;
        delay(10);
  }
   Serial.flush();
   delay(100);
}
void receiveData() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc; 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void parseData() {      // split the data into its parts
    Serial.flush();
    char * strtokIndx; // this is used by strtok() as an index
    strtokIndx = strtok(tempChars, ","); // this continues where the previous call left off
    deviceId = atoi(strtokIndx);
    Serial.print("device_id: ");
    Serial.println(deviceId);
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    measurementId = atoi(strtokIndx);     // convert this part to an integer
    Serial.print("measurement_id: ");
    Serial.println(measurementId);
    strtokIndx = strtok(NULL, ",");
    measurementValue = atof(strtokIndx);    // convert this part to a float
    Serial.print("measurement_value: ");
    Serial.println(measurementValue);
    showParsedData();
    sendReading();
    Serial.flush();
}

void showParsedData() {
    StaticJsonBuffer<1024> JSONbuffer;
    JsonObject& JSONencoder = JSONbuffer.createObject();
    JSONencoder["device_id"] = deviceId;
    JSONencoder["measurement_id"] = measurementId;
    JSONencoder["measured_value"] = measurementValue;
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
}

void sendReading() {
  HTTPClient http;
  http.begin("http://maxwell.casa/record_sensor_reading"); 
  http.addHeader("Content-Type", "application/json");
  String payload = http.getString();
  int httpCode = http.POST(JSONmessageBuffer);
  Serial.println(httpCode);
  http.end();
  }
