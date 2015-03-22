import sqlite3

connection = sqlite3.connect('priceData.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM priceData WHERE itemPrice = 150")
data = cursor.fetchall()

if len(data) == 0:
    print "nothing there"

    
#cursor.execute("INSERT INTO priceData values(1, 150)")
connection.commit()
connection.close()
exit()
