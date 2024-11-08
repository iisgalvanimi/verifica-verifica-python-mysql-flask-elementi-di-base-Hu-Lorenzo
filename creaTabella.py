import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Vegetali"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE Verdure (id INT PRIMARY KEY,Nome VARCHAR(255),Colore VARCHAR(255),Parte_edibile VARCHAR(255),Stagione VARCHAR(255),Calorie INT)")
mydb.close()
