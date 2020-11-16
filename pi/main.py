import w1thermsensor
from CharLCD import CharLCD
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import spidev
import time

lcd = CharLCD()
sensor = w1thermsensor.W1ThermSensor()
externalSensorError = 'Brak'
lcdMessage = 'Dom: {} \nNa dworze: {}'

lcd.begin(16,1)

GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.powerUp()

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

# radio.openReadingPipe(1, [140, 120, 0xf0, 0xf0, 0xe1])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

current_temp=0.0
while 1:
 while not radio.available(0):
  time.sleep(1/100)

 receivedMessage = []
 radio.read(receivedMessage, radio.getDynamicPayloadSize())
 string = ""
 # pdb.set_trace()
 for n in receivedMessage:
  if(n >= 32 and n <= 126):
   string += chr(n)
 print("Received:{}".format(string))
 temp = round(sensor.get_temperature(), 1)
 if current_temp != temp:
   lcd.clear()
   lcd.message(lcdMessage.format(str(temp), externalSensorError))
   current_temp = temp

sleep(2)
