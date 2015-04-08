# -*- coding: utf-8 -*-
import model
import lcd
import time
import keypad

currentMenu = 0

def main():
    #this is the 'main' function, when the user presses something on the device they go to a differnt menu, when they need
    #to change menu the function of the menu they are using returns the correct value for the menu they want to move to
    while True:
        global currentMenu
        if currentMenu == 0:
            currentMenu = home()
        elif currentMenu == 1:    
            currentMenu = priceGet(False)
        elif currentMenu == 2:
            print("Now Editing")
            currentMenu = edit("why not worky")
        elif currentMenu == 3:
            currentMenu = newItem()
        #time.sleep(1)
    
        

def home():
    #This is the home menu, the program starts here
    #This menu is essentially a gateway to other menus and their functions
    
    while True:
        print("should not be here")
        lcd.display("PRICE: * NEW: 0", 0)
        lcd.display("EDIT: #", 1)
        #gets the users choice
        choice = keypad.getKey()
        #returns the value associated with the desired menu, so the main function can change to
        #that menu
        if choice == "*":
            return 1
        elif choice == "#":
            return 2
        elif choice == "0":
            return 3
        else:
            #this plays havoc with the LCD i have no idea why
            lcd.display("Invalid input", 0)
            lcd.display("Enter a * or #", 1)
            print("")
        
def priceOrderer(price, mode):
    #this function takes in a unformated price, for example 199
    #and then returns it formated like: $1.99
    #It has 2 different modes
    tempPriceArray = list(price)
    finalPrice = ""
    if mode != 1:
        if len(tempPriceArray) == 1:
            finalPrice = price
            finalPrice +="p"
        
        if len(tempPriceArray) == 2:
            finalPrice = price
            finalPrice += "p"
    if mode == 1:
        if len(tempPriceArray) == 1:
            finalPrice = "$"
            finalPrice += "0"
            finalPrice += "."

            finalPrice += "0"
            finalPrice += tempPriceArray[0]
        if len(tempPriceArray) == 2:
            finalPrice = "$"
            finalPrice += "0"
            finalPrice += "."

            finalPrice += tempPriceArray[0]
            finalPrice += tempPriceArray[1]     
            
    if len(tempPriceArray) == 3:

        finalPrice = "$"
        finalPrice += tempPriceArray[0]
        finalPrice += "."

        finalPrice += tempPriceArray[1]
        finalPrice += tempPriceArray[2]
        

    if len(tempPriceArray) == 4:
        finalPrice = "$"
        finalPrice += tempPriceArray[0]
        finalPrice += tempPriceArray[1]
        finalPrice += "."

        finalPrice += tempPriceArray[2]
        finalPrice += tempPriceArray[3]
        lcd.display("PRICE: "+finalPrice, 0)
        
        lcd.display("BACK: *", 1)    
    return finalPrice
def priceGet(modulus):
    print("At price get")
    serialNumber = barcodeInput()
    if serialNumber == False:
        if modulus:
            return 0, 0
        else:
            return 0
    price = model.getPrice(serialNumber)
    

    if price == False:
        lcd.display("Barcode not", 0)
        lcd.display("recognised", 1)
        time.sleep(2)
        if modulus:
            print("Returning 0, 0")
            return 0, 0
        else:
            return 0
    price = str(price)
    finalPrice = priceOrderer(price, 0)
    if modulus == False:
        
        
        lcd.display("PRICE: "+finalPrice, 0)
            
        lcd.display("BACK: *", 1)
        print(finalPrice)
        while True:
            key = keypad.getKey()
            if key == "*":
                return 0
    if modulus == True:
        
        
        return finalPrice, serialNumber 
        

    
    

def barcodeInput():
    lcd.display(" ", 0)
    lcd.display("BACK: * ENTER: #", 1)
    serialNumber = ""
    
    while True:
        print("inputing Now")
        key = keypad.getKey()
        if key == "*":
            if len(serialNumber) == 0:
                return False
            serialNumber = serialNumber[:-1]
            lcd.display(str(serialNumber), 0)
            
        elif key == "#":
            return serialNumber
            
        else:
            print("serialNumber")
            print(serialNumber)
            serialNumber += str(key)
            lcd.display(str(serialNumber), 0)
        
def edit(tempError):
    print(tempError)
    print("At Edit")

    
    oldPrice, serialNumber = priceGet(True)
    print("PPringting stuff")
    print(oldPrice)
    print(serialNumber)

    

    
    if serialNumber == 0 and oldPrice == 0:
        print("WHY AM I NOT HERE")
        return 0
    
    
    lcd.display("OLD: "+oldPrice+" NEW:", 0)
    lcd.display("$0.00 ENTER: #", 1)
    price = ""
    exitLoop = False
    while exitLoop == False:
        key = keypad.getKey()
        if key == "#":
            exitLoop = True
        elif key == "*":
            if len(price) == 0:
                return 0
            price = price[:-1]
        else:
            price +=key
        print("Now printing price")
        print(price)
        print("Now printing fnalPrice")
        
        finalPrice = priceOrderer(price, 1)
        print(finalPrice)
        lcd.display(finalPrice+" ENTER: #", 1)
    model.edit(serialNumber, price)
    lcd.display("SUCCESS", 0)
    lcd.display(" ", 1)
    time.sleep(1)
    return 0
def newItem():
    serialNumber = ""
    temp = True
    temp = barcodeInput()
    if temp == False:
        return 0
    serialNumber += temp
    print("Now printing serial number")
    print(serialNumber)
    if serialNumber == False:
        return 0
    
    exitLoop = False
    price = ""
    lcd.display("PRICE: $0.00", 0)
    lcd.display("BACK: * ENTER: #", 1)
    while exitLoop == False:
        key = keypad.getKey()
        if key == "#":
            exitLoop = True
        elif key == "*":
            if len(price) == 0:
                return 0
            price = price[:-1]
        else:
            price +=key
        print("Now printing price")
        print(price)
        print("Now printing fnalPrice")
        
        finalPrice = priceOrderer(price, 1)
        print(finalPrice)
        lcd.display("PRICE: "+finalPrice, 0)
        lcd.display("BACK: * ENTER: #", 1)
    result = model.newItem(serialNumber, price)
    if result:
        lcd.display("SUCCESS", 0)
        lcd.display("", 1)
    else:
        lcd.display("ITEM ALLREADY", 0)
        lcd.display("EXISTS", 1)
    return 0    
if True:
    main()
    
        
        
    
    
    
    
    






























        
        

def edit():
    return None


if True:
    main()
