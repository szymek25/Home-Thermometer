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

lcd.begin(16, 1)

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
radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])
radio.printDetails()

current_temp = 0.0
external_currentTemp = 0.0
timeOut = False

command = list("GETTEMPERATURE")
#Message has size of 32 bits, at the end zero needs to be appended
while len(command) < 32:
    command.append(0)

while 1:

    start = time.time()
    radio.write(command)
    radio.startListening()
    while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start > 2:
            print("Timed out.")
            timeOut = True
            break

    if not timeOut:
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        externalTempString = ""

        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                externalTempString += chr(n)
        print("Received:{}".format(externalTempString))
        externalTemp = round(float(externalTempString), 1)
    else:
        externalTemp = externalSensorError

    temp = round(sensor.get_temperature(), 1)
    if current_temp != temp or external_currentTemp != externalTemp:
        lcd.clear()
        lcd.message(lcdMessage.format(str(temp), externalTemp))
        current_temp = temp
        external_currentTemp = externalTemp

    timeOut = False
    radio.stopListening()
    time.sleep(2)
