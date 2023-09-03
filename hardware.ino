#include <OneWire.h>
#include <DallasTemperature.h>

#define LED1 13
#define LED2 33
#define ONE_WIRE_BUS 32
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, 0);
  digitalWrite(LED2, 0);
  sensors.begin();
  Serial.begin(115200);
}

void loop() {
  String val = "";
  while (Serial.available() > 0) {  // WARNING: Serial data flow from pc must be continiuous, no delay is allowed , otherwise the control will be a disaster!
    int inChar = Serial.read();
    val += (char)inChar;
    if (inChar == '\n') {
      int comma = val.indexOf("-");
      int semicomma = val.indexOf(";");
      String device = (val.substring(0, comma));
      int value = 0;
      if (device != "rtemp") {
        value = (val.substring(comma + 1, semicomma)).toInt(); //converts string to int for speed value
      } else {
        sensors.requestTemperatures();
        Serial.print(String(sensors.getTempCByIndex(0)));
      }
      val = "";
      if (device == "light01") {
        digitalWrite(LED1, value);
      }
      else if (device == "light02") {
        digitalWrite(LED2, value);
      }
    }
  }
}
