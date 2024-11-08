from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',     
    'user': 'root',      
    'password': '', 
    'database': 'Vegetali'
}

@app.route('/dati', methods=['GET'])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Verdure")
        result = cursor.fetchall()
        return jsonify(result)
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile connettersi al database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
@app.route('/dati/aggiungi', methods=['POST'])
def aggiungi_dati():
    try:
        dati = request.get_json()
        required_fields = ['Nome', 'Colore', 'Parte_edibile', 'Stagione', 'Calorie']
        if not dati or not all(field in dati for field in required_fields):
            return jsonify({"errore": "Dati incompleti"}), 400
        nome = dati['Nome']
        colore = dati['Colore']
        parte_edibile = dati['Parte_edibile']
        stagione = dati['Stagione']
        calorie = dati['Calorie']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO Verdure (Nome, Colore, Parte_edibile, Stagione, Calorie) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, colore, parte_edibile, stagione, calorie))
        conn.commit()

        return jsonify({"messaggio": "Dati inseriti con successo"}), 201
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": f"Errore nel database: {str(e)}"}), 500
    
    except Exception as e:
        print("Errore generico:", e)
        return jsonify({"errore": f"Si è verificato un errore: {str(e)}"}), 500
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
 app.run()