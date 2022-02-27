# PgP 7/30/2020
# SystemTest.py
# mashup of programs from Dexter industries/SEEED Studios
# Test of WSU COB Somsen 301 GrovePi+ system
# Press button to start test of all sensors and actuators
# Display test results in command line, write output to log file, and use text to speech engine to pronounce results

# have default statement at first, but later once button pushed, user can type in text 
# it works over sound out 3.5mm port, but need to figure out how to send to HDMI output
# code needs to be cleaned up
# make sure audio outputs are set correctly-HDMI or analog

#!/usr/bin/env python


import os
import random
import time
import grovepi
import sys
import datetime
from subprocess import call
from grove_rgb_lcd import *


from grovepi import *

# Assign ports for all sensors and actuators

light_sensor = 0           # Analog  Port for Light sensor
potentiometer = 1          # Analog  Port for Rotary Angle sensor
sound_sensor = 2           # Analog  Port for Sound sensor

ultrasonic_ranger = 2      # Digital Port for Ultrasonic Ranger sensor
buzzer_pin=3               # Digital Port for Buzzer actuator
button=4                   # Digital Port for Button actuator
dht_sensor_port = 5        # Digital Port for DHT sensor
dht_sensor_type = 0        # use 0 for the blue-colored sensor and 1 for the white-colored sensor
ledbar = 6                 # Digital Port for LED Bar actuator

relay = 8                  # Digital Port for Relay

pinMode(button, "INPUT")   # Assign Button as input
pinMode(buzzer_pin,"OUTPUT")  #Assign Buzzer as output
pinMode(relay,"OUTPUT")    # Assign Relay as output
pinMode(potentiometer,"INPUT")  #Assign Potentiometer as input
pinMode(sound_sensor,"INPUT")  # Assign Microphone as input


#################################################################
## Create Log File Location

log_file="/home/pi/Desktop/SystemTest.txt"     # This is the name of the file we will save data to.
                                                        # This is hard coded to the Desktop.
# write file header line
f=open(log_file,'a')
now = datetime.datetime.now()
f.write("Systen test began on " + now.strftime("%Y-%m-%d %H:%M:%S") + "\n" )
f.write("test data\n")
print("Saving system test data to the file:", log_file )

#################################################################



#Calls the Espeak TTS Engine to read aloud a sentence
def sound(spk):
    #   -ven+m7:    Male voice
    #   -s180:      set reading to 180 Words per minute
    #   -k20:       Emphasis on Capital letters
    cmd_beg=" espeak -ven+m7 -a 200 -s180 -k20 --stdout '"
    cmd_end="' | aplay"
    print (cmd_beg+spk+cmd_end)
    call ([cmd_beg+spk+cmd_end], shell=True)



def createMessage(message):
    try:
        # message= "Welcome to another exciting edition of M I S !"
        # lcd_rgb(str(message))
        # led_random()
        sound(message)
        print(message)
    except TypeError:
        print ("Message Error! Data Type Error!")
    except IOError:
        print ("Message Error! Input Output Error!")

 


strSpeak = "Grove Pi firm ware version: " + grovepi.version()
print(strSpeak)
createMessage(strSpeak)


strSpeak = "Press the button to start the test"
print(strSpeak)
createMessage(strSpeak)  

time.sleep(.2)

button_status=digitalRead(button)

# while True:
while button_status==0 :
    
    button_status=digitalRead(button) # Read button status
    
    # button_status = 1 # insert for testing purposes, so do not have to press button
    
    if button_status:  # if button status HIGH, button is pushed, so run the program
        
        # for testing purposes, assume button is pressed
        button_status = 0  # release button

        digitalWrite(buzzer_pin,0) # silence buzzer
        
       # Test 1-buzzer-digital and analog 
        
        strSpeak = "Test number 1, buzzer, digital first, then analog"
        print(strSpeak)
        createMessage(strSpeak)
        f.write(strSpeak + "\n")
 
        digitalWrite(buzzer_pin,1)  # digital write is either on or off, 0 or 1
        time.sleep(.25)
        digitalWrite(buzzer_pin,0)
        time.sleep(.25)
        analogWrite(buzzer_pin, 2)   # analog write can vary-0 is off, levels from 1 to 255
        time.sleep(.25)
        analogWrite(buzzer_pin, 64)
        time.sleep(.25)
        analogWrite(buzzer_pin, 128)
        time.sleep(.25)
        analogWrite(buzzer_pin, 196)
        time.sleep(.25)        
        analogWrite(buzzer_pin,0)  #silence buzzer
        
        
        # Test 2-ultrasonic ranger
        distance = (ultrasonicRead(ultrasonic_ranger))
        inches =str(int(distance / 2.54))
                
        strSpeak = ("Test number 2,  Ultrasonic ranger, which indicates distance to object of " + inches + " inches")
        print(str(strSpeak))
        createMessage(str(strSpeak))
        f.write(strSpeak + "\n")
        
        # Test 3- Tenperature and Humidity sensor
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
        
        temperature = str(int(temp * 9 / 5 + 32))
        humidity = str(int(hum))
        
        strSpeak = ("Test number 3, temperature and humidity sensor, which indicates a current temperature of " + temperature + " degrees Fahrenheit, and a humidity of " + humidity + " per cent")
        print(strSpeak)
        createMessage(strSpeak)
        f.write(strSpeak + "\n")
        
        # Test 4- LED Bar
        
        strSpeak = ("Test number 4, L E D bar, which will turn on one bar at a time until they are all lit up")
        print(strSpeak)
        createMessage(strSpeak)
        f.write(strSpeak + "\n")
        
        bar_level = 0  
        grovepi.pinMode(ledbar,"OUTPUT")
        time.sleep(1)
        
             
        grovepi.ledBar_setLevel(ledbar, 1)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 2)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 3)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 4)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 5)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 6)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 7)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar,8)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 9)
        time.sleep(.1)
        grovepi.ledBar_setLevel(ledbar, 10)
        time.sleep(.5)
        grovepi.ledBar_setLevel(ledbar,0)
        time.sleep(.1)
        
        # Test 5, RGB screen
        
        strSpeak = ("Test number 5, R G B screen, which will change background colors, then print this message")
        print(strSpeak)
        createMessage(strSpeak)
        f.write(strSpeak + "\n")
        
        setText_norefresh("")
        setRGB(0,0,255)  #blue
        time.sleep(.5)
        setRGB(255,0,0) #red
        time.sleep(.5)
        setRGB(0,255,0) # green
        time.sleep(.5)
        setRGB(128,128,128) # gray
        time.sleep(.5)
        setRGB(255,255,255) #white
        time.sleep(.5)
        setRGB(0,0,0) # off
        time.sleep(.1)
        setText_norefresh(strSpeak)
        setRGB(128,138,128)
        time.sleep(1)
        setRGB(0,0,0)
        setText_norefresh("") #clear any messages on screen
        
        
        
        # Test 6, relay
        strSpeak = ("Test number 6, cycle Relay twice, red light indicates closed relay")
        print(strSpeak)
        createMessage(strSpeak)        
        f.write(strSpeak + "\n")        
        
        grovepi.digitalWrite(relay,1)
        time.sleep(1)
        print("button pushed, relay closed, connection made, light on")

        grovepi.digitalWrite(relay,0)
        time.sleep(.5)
        print("button released, relay open, connection broken")       
        
        grovepi.digitalWrite(relay,1)
        time.sleep(1)
        print("button pushed, relay closed, connection made, light on")

        grovepi.digitalWrite(relay,0)
        time.sleep(.5)
        print("button released, relay open, connection broken")
        
     
        
        
        # Test 7, light sensor
        
        light=str(grovepi.analogRead(light_sensor))
                
        strSpeak = ("Test number 7, light sensor, which indicates an ambient light level of  " + light)
        print(strSpeak)
        createMessage(strSpeak)
        f.write(strSpeak + "\n")        
        
        
        # Test 8, potentiometer
        
        strSpeak = ("Test number 8, rotary potentiometer, turn the dial to display the angle of rotation on the r g b panel. Press button to stop." )
        print(strSpeak)
        createMessage(strSpeak)        
        f.write(strSpeak + "\n")
        
        # Reference voltage of ADC is 5v
        adc_ref = 5

        # Vcc of the grove interface is normally 5v
        grove_vcc = 5

        # Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
        full_angle = 300
        
        setText_norefresh("") #clear any messages on screen        

        while button_status==0 :
            try:
                # Read sensor value from potentiometer
                sensor_value = grovepi.analogRead(potentiometer)
                f.write("light sensor value: " + str(sensor_value) + "\n")

                # Calculate voltage
                voltage = round((float)(sensor_value) * adc_ref / 1023, 2)

                # Calculate rotation in degrees (0 to 300)
                degrees = round((voltage * full_angle) / grove_vcc, 2)

                print("sensor_value = %d   voltage = %.2f   degrees = %.1f " %(sensor_value, voltage, degrees))
                
                setRGB(128,128,128)
                setText_norefresh(str(int(degrees)))
                button_status=digitalRead(button)
                
       
            except KeyboardInterrupt:
                #grovepi.analogWrite(led,0)
                break
            except IOError:
                print ("Error")
        setRGB(0,0,0)
        setText("")
        
        
        
        
# Test 9, microphone
sound_value = grovepi.analogRead(sound_sensor)
soundValue = str(int(sound_value))
        
strSpeak = ("Test number 9, sound sensor, which indicates an ambient sound level of " + soundValue )
print(strSpeak)
createMessage(strSpeak)
f.write(strSpeak + "\n")
 
 
# end of tests
strSpeak = ("All tests complete.  The log file, system test dot t x t is available on the desktop.")
createMessage(strSpeak)

f.write("System test ended at " + now.strftime("%Y-%m-%d %H:%M:%S") + "\n" )
#strSpeak = ("Sensor and actuator tests are complete. \n The log file sensors.txt is available on the desktop.")
#createMessage(strSpeak)
#f.write(strSpeak + "\n")

f.close()


