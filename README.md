# Home-Thermometer

Hobby project for learning something after job.
Code with connected remote thermometer can be found here: https://github.com/szymek25/Remote-Thermometer

# Connection matrix

## LCD  Raspberry PI
1    GND  
2    5V  
3    Potentiometer  
4    #23  
5    GND  
6    #24  
7  
8  
9  
10  
11   #25  
12   #12  
13   #20  
14   #21  
15   output from X9C103S  
16   GND  


## DS18B20  PI
GND  GND  
VCC  3V  
DAT  #4  

## NRF24L01 PI
VCC 3V  
GND GND  
CSN CE0  
CE  #17  
MOSI MOSI  
SCK SCLK  
IRQ none   
MISO MISO  

## X9C103S PI
CS #6  
INC #19  
UD #13  
