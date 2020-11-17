#include <OneWire.h>
#include <DallasTemperature.h>
#include <SPI.h>
#include <RF24.h>
#include <string.h>
RF24 radio(9,10);

OneWire oneWire(A5); //Podłączenie do A5
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();

}

void loop() {
  sensors.requestTemperatures();//Pobranie temperatury czujnika
  char text[5];
  float temp = sensors.getTempCByIndex(0);
  String tempString;
  tempString = String(temp);
  strcpy(text, tempString.c_str());
  radio.write(&text, sizeof(text));
  delay(5000);
 
}
