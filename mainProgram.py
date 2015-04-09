# -*- coding: utf-8 -*-
import model
import lcd
import time
import keypad

currentMenu = 0
#A BARCODE AND A SERIAL NUMBER ARE THE SAME THING
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
            currentMenu = edit()
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
    #It has 2 different modes, when mode is 0 a price of 080 would be converted to 80p
    #when mode is 1 it will be converted to $0.80
    tempPriceArray = list(price) #the price string is turned in to an array of characters as it allows me
    #to add a certain digit in the price string to a certain place, for example betweem a $ and a . easier
    finalPrice = "" #this is what is eventuly returned/displayed
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
    #this function can act as its own "menu", or it can be used by other "menus" to return theprice of an item, for example if I wanted 
    #to get the price of something i would use this menu, if I wanted to edit the price I would use the edit menu,
    #which would call this function to get the price to show you before you change it.
    #if modulus is true then it returns the price
    #otherwise it displays it on the screen and acts as its own menu
    
    
    print("At price get")
    #calls the barcodeInput function to get the serialNumber of the item whos price is wanted
    serialNumber = barcodeInput()
    if serialNumber == False: #false will be returned from the barcodeInput function if the user wants to go back
    #so, if priceGet is being used in a not modulus fashion it will return 0 to main, taking us back to the main menu
    #otherwise it will return 0, 0 to the menu that called it and that menu will decide what to do with it
    #specifically
        if modulus:
            return 0, 0
        else:
            return 0 #
    price = model.getPrice(serialNumber)#This searches the database for the serialNumber the user has inputed
    

    if price == False: #false will be returned if the barcode does not exist
        lcd.display("Barcode not", 0)
        lcd.display("recognised", 1)
        time.sleep(2)
        if modulus:
            print("Returning 0, 0")
            return 0, 0
        else:
            return 0
    price = str(price)
    finalPrice = priceOrderer(price, 0)#orders the returned price, uses mode 0 as in this case we would prefer 60p to $0.60
    
    if modulus == False:
        
        
        lcd.display("PRICE: "+finalPrice, 0) #displays the price
            
        lcd.display("BACK: *", 1)
        print(finalPrice)
        while True:#waits for the user to press *, so they can return to the main menu
            key = keypad.getKey()
            if key == "*":
                return 0
    if modulus == True: #or returns the price to the function that called it
        
        
        return finalPrice, serialNumber 
        

    
    

def barcodeInput():
    lcd.display(" ", 0)
    lcd.display("BACK: * ENTER: #", 1)
    serialNumber = ""
    
    while True:
        print("inputing Now")
        key = keypad.getKey()#gets the what key is pressed one by one
        
        if key == "*":#this little bit here allows 2 things, if the user had accidently pressed the wrong key they can press *
        #to delete it
            if len(serialNumber) == 0:#or, if the everything has been deleted and they press * again it means they
            #want to go back so False is returned, so the function in use can handle that
                return False
            serialNumber = serialNumber[:-1]#subtracts 1 character from the barcode
            lcd.display(str(serialNumber), 0)#and displays the new barcode
            
        elif key == "#":#this is an enter key essentially
        #when the user presses this it means they have entered all the digits of the barcode
            return serialNumber 
            
        else:
            
            print("serialNumber")
            print(serialNumber)
            serialNumber += str(key)#adds the key that has been entered to the serial number
            lcd.display(str(serialNumber), 0)#prints the barcode as it is being entered, so the user can see
        
def edit():
    
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
