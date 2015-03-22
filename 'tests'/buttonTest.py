import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.IN)
while True:
        if(GPIO.input(37) == False):
            print "ON"
        else:
            print("OFF")
            
        time.sleep(0.5)    
