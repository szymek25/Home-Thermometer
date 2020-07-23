#include <OneWire.h>
#include <DallasTemperature.h>

OneWire oneWire(A5); //Podłączenie do A5
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures(); //Pobranie temperatury czujnika
  Serial.print("Aktualna temperatura: ");
  Serial.println(sensors.getTempCByIndex(0));  //Wyswietlenie informacji
  delay(500);
}
