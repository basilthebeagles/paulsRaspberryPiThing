# #####################################################
# Python Library for 3x4 matrix keypad using
# 7 of the avialable GPIO pins on the Raspberry Pi. 
# 
# This could easily be expanded to handle a 4x4 but I 
# don't have one for testing. The KEYPAD constant 
# would need to be updated. Also the setting/checking
# of the colVal part would need to be expanded to 
# handle the extra column.
# 
# Written by Chris Crumpacker
# May 2013
#
# main structure is adapted from Bandono's
# matrixQPI which is wiringPi based.
# https://github.com/bandono/matrixQPi?source=cc
# #####################################################
 
import RPi.GPIO as GPIO
import time 
# CONSTANTS   
KEYPAD = [
[1,2,3],
[4,5,6],
[7,8,9],
["*",0,"#"]
]
     
ROW         = [15,18,32,11] 
COLUMN      = [13,16,12]
lastKey = ""     
#set it so the gpio's are referenced by their boardnumber   
GPIO.setmode(GPIO.BOARD)
     
    
def keyCheck(): 
    # Set all columns as output low
    for j in range(len(COLUMN)):
        GPIO.setup(COLUMN[j], GPIO.OUT)
        GPIO.output(COLUMN[j], GPIO.LOW)
        
         
        # Set all rows as input
    for i in range(len(ROW)):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
    rowVal = -1
    for i in range(len(ROW)):
        tmpRead = GPIO.input(ROW[i])
         
        if tmpRead == 0:
            print('Oooh somethings pressed!')
            rowVal = i
                 
        #if rowVal is not 0 thru 3 then no button was pressed and we can exit
    if rowVal <0 or rowVal>3:
            
        return 99
         
        # Convert columns to input
    for j in range(len(COLUMN)):
        GPIO.setup(COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Switch the i-th row found from scan to output
    GPIO.setup(ROW[rowVal], GPIO.OUT)
    GPIO.output(ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
    colVal = -1
    for j in range(len(COLUMN)):
        
        tmpRead = GPIO.input(COLUMN[j])
        if tmpRead == 1:
            
            colVal=j
                 
         #if colVal is not 0 thru 2 then no button was pressed and we can exit
    if colVal < 0 or colVal > 2: 
            
        return 99
 
        # Return the value of the key pressed
    exit()
    return KEYPAD[rowVal][colVal]
         
def exit():
    
        # Reinitialize all rows and columns as input at exit
    for i in range(len(ROW)):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    for j in range(len(COLUMN)):
        GPIO.setup(COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         

    

     
    # Loop while waiting for a keypress
def getKey():
    global lastKey
    key = None
    while True:
        temp = keyCheck()
        if temp != 99:
            time.sleep(0.8) 
            key = str(temp)
            
            print(key)
            lastKey = key
            return key
        time.sleep(0.1)    
        # Print the result
    
   
