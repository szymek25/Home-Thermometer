# X9C103.py
# Author - Srikanth Sugavanam, IIT Mandi, India - 26th January 2022

# This module is written for controlling the X9C103 digital potentiometer with
# a Raspberry Pi. This is a code in development, and will be updated from
#time to time. Please refer to the original datasheet for more information
#on the pin layout and timing diagram information, which forms the basis for
#this library/module. BCM - Broadcom board numbering

#Code flowchart
#===============
#INITIATE
# 0. CS is high, INC is high.
#ACTIVATE
# 1. Select chip by setting CS to low.
# 2. Sleep 1 us. (As tCI - 0.1 us)
#WIPERSET
# 3. Set U/D level
# 4. Sleep 4 us. (As tDI - 2.9 us)
#WIPERMOVE
# 5. Toggle INC from high to low.
# 6. Sleep for 100 us. (As tIW is 100 us)
#DISCONNECT
# 7. Return INC to high. 
# 8. Sleep 4 us (As tIC - 1 us)
# 9. Set CS high to store resistance value


import RPi.GPIO as GPIO
from time import sleep

def initiate(CS,INC,UD):
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CS,GPIO.OUT)
    GPIO.setup(INC,GPIO.OUT)
    GPIO.setup(UD,GPIO.OUT)
    
    
    GPIO.output(CS,GPIO.HIGH)
    GPIO.output(INC,GPIO.HIGH)
    GPIO.output(UD,GPIO.LOW)

    print('Pins set as per BCM board numbering convention.')
    
def activate(CS,INC,UD):
    GPIO.output(CS,GPIO.LOW)
    sleep(0.000001)
    print('Chip activated')

def wiperset(CS,INC,UD,flag):
    
    if flag == True:
        GPIO.output(UD,GPIO.HIGH)
    else:
        GPIO.output(UD,GPIO.LOW)
        
    sleep(0.000005)
    print('Wiper move direction set')

def wipermove(CS,INC,UD,step):
    
    for ii in range(step):

        #Moving the wiper
        #REPEAT the following code snippet as many times you want to move the wiper
        #===================================================================================
        GPIO.output(INC,GPIO.LOW)     #Set INC to low to move wiper
        sleep(0.000100)               #Wait for voltage level to settle

        GPIO.output(INC,GPIO.HIGH)    #Pull INC to high for next cycle
        sleep(0.000002)               #Minimum wait time before INC can be pulled low again

        sleep(0.0001)
#         sleep(delay)

    #GPIO.output(UD,GPIO.LOW)
    sleep(0.000005)
    print("Sweep has ended")

def reset(CS,INC,UD):
    
    input("The pot will now sweep the wiper. Please disconnect circuit if required and press enter to continue: ")
    wiperset(CS,INC,UD,1)
    wipermove(CS,INC,UD,99)
    
    wiperset(CS,INC,UD,0)
    wipermove(CS,INC,UD,99)
    
    
def disconnect(CS,INC,UD):
    #Deselecting the chip
    GPIO.output(INC,GPIO.HIGH)
    sleep(0.000004)               #Time interval to allow the chip to settle before moving CS to high
    GPIO.output(CS,GPIO.HIGH)
    GPIO.cleanup()
    print('Potentiometer disconnected.')

