import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Vegetali"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM Verdure")

myresult = mycursor.fetchall()
for x in myresult:
    print(x)