#include <OneWire.h>
#include <DallasTemperature.h>
#include <SPI.h>
#include <RF24.h>
#include <printf.h>
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
  const char text[] = "Hello World!";
  radio.write(&text, sizeof(text));
  
  sensors.requestTemperatures(); //Pobranie temperatury czujnika
  Serial.print("Aktualna temperatura: ");
  Serial.println(sensors.getTempCByIndex(0));  //Wyswietlenie informacji
  delay(1000);
 
}
