import w1thermsensor
from CharLCD import CharLCD

lcd = CharLCD()
sensor = w1thermsensor.W1ThermSensor()
externalSensorError = 'Brak'
lcdMessage = 'Dom: {} \nNa dworze: {}'

lcd.begin(16,1)

current_temp=0.0
while 1:
 temp = round(sensor.get_temperature(),1)
 if current_temp != temp:
   lcd.clear()
   lcd.message(lcdMessage.format(str(temp), externalSensorError))
   current_temp = temp

sleep(2)
