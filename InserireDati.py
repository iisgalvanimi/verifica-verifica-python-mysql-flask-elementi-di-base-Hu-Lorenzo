
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Vegetali"
)

mycursor = mydb.cursor()

sql = "INSERT INTO Verdure (Nome,Colore,Parte_edibile,Stagione,Calorie) VALUES (%s, %s,%s, %s,%s)"
val = [
    ('Carota', 'Arancione', 'Radice', 'Tutto l\'anno', '41'),
    ('Spinaci', 'Verde', 'Foglie', 'Tutto l\'anno', '23'),
    ('Pomodoro', 'Rosso', 'Frutto', 'Estate', '18'),
    ('Cetriolo', 'Verde', 'Frutto', 'Estate', '16'),
    ('Zucchina', 'Verde', 'Frutto', 'Estate', '17'),
    ('Patata', 'Gialla', 'Tubercolo', 'Tutto l\'anno', '77'),
    ('Cipolla', 'Bianca', 'Bulbo', 'Tutto l\'anno', '40'),
    ('Broccolo', 'Verde', 'Fiore', 'Inverno', '34'),
    ('Cavolfiore', 'Bianco', 'Fiore', 'Inverno', '25'),
    ('Lattuga', 'Verde', 'Foglie', 'Tutto l\'anno', '15')
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")