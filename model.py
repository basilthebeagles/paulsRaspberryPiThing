import sqlite3

connection = sqlite3.connect('priceData.db')


def newItem(serialNumber, itemPrice):
    cursor = connection.cursor()
    print(serialNumber)
    print(itemPrice)
    if verify(serialNumber):
        return False
    print(("INSERT INTO priceData values ("+ str(serialNumber)+", "+ str(itemPrice)+");"))
    cursor.execute("INSERT INTO priceData values ("+ str(serialNumber)+", "+ str(itemPrice)+");")
    connection.commit()
    return True

def edit(serialNumber, newPrice):

    cursor = connection.cursor()
    if verify(serialNumber) == False:
        return False
    
    cursor.execute("UPDATE priceData SET itemPrice = "+str(newPrice)+" WHERE serialNumber = "+str(serialNumber))
    connection.commit()
    
def getPrice(serialNumber):
    cursor = connection.cursor()
    if verify(serialNumber)== False:
        return False
    
    cursor.execute("SELECT itemPrice FROM priceData WHERE serialNumber = "+str(serialNumber))
    row = cursor.fetchone()
    
    data = row[0]
    return data
        
def verify(serialNumber):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM priceData WHERE serialNumber = "+str(serialNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True
    
def close():
    connection.close()
    
