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
@app.route('/dati/<filtro>/<valore>', methods=['GET'])
@app.route('/dati/<filtro>/<valore_min>/<valore_max>', methods=['GET'])
def get_data(filtro=None, valore=None, valore_min=None, valore_max=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Verdure" 
        params = ()

        if filtro and valore and not valore_min and not valore_max:
            if filtro in ['id', 'Nome', 'Colore', 'Parte_edibile', 'Stagione', 'Calorie']:
                query += f" WHERE {filtro} = %s"
                params = (valore,)
        
        elif filtro and valore_min is not None and valore_max is not None:
            if filtro in ['Calorie']:  
                query += f" WHERE {filtro} BETWEEN %s AND %s"
                params = (valore_min, valore_max)

        cursor.execute(query, params)
        result = cursor.fetchall()
        return jsonify(result)

    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": f"Errore nel database: {str(e)}"}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
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
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
@app.route('/dati/elimina/<int:id>', methods=['DELETE'])
def elimina_dati(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "DELETE FROM Verdure WHERE id = %s"
        cursor.execute(query, (id,))

        if cursor.rowcount == 0:
            return jsonify({"errore": f"Nessun record trovato con id {id}"}), 404

        conn.commit()

        return jsonify({"messaggio": f"Record con id {id} eliminato con successo"}), 200
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": f"Errore nel database: {str(e)}"}), 500
    
    except Exception as e:
        print("Errore generico:", e)
        return jsonify({"errore": f"Si è verificato un errore: {str(e)}"}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/dati/aggiorna/<int:id>', methods=['PUT'])
def aggiorna_dati(id):
    try:
        dati = request.get_json()
        if not dati or not any(k in dati for k in ['Nome', 'Colore', 'Parte_edibile', 'Stagione', 'Calorie']):
            return jsonify({"errore": "Dati incompleti"}), 400
        
        nome = dati.get('Nome')
        colore = dati.get('Colore')
        parte_edibile = dati.get('Parte_edibile')
        stagione = dati.get('Stagione')
        calorie = dati.get('Calorie')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE Verdure SET"
        updates = []

        if nome:
            updates.append(" Nome = %s")
        if colore:
            updates.append(" Colore = %s")
        if parte_edibile:
            updates.append(" Parte_edibile = %s")
        if stagione:
            updates.append(" Stagione = %s")
        if calorie:
            updates.append(" Calorie = %s")

        if not updates:
            return jsonify({"errore": "Nessun campo da aggiornare"}), 400

        query += ",".join(updates) + " WHERE id = %s"
        params = tuple(valore for valore in [nome, colore, parte_edibile, stagione, calorie] if valore is not None) + (id,)

        cursor.execute(query, params)

        conn.commit()

        return jsonify({"messaggio": f"Dati aggiornati per id {id} con successo"}), 200
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": f"Errore nel database: {str(e)}"}), 500
    
    except Exception as e:
        print("Errore generico:", e)
        return jsonify({"errore": f"Si è verificato un errore: {str(e)}"}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
if __name__ == '__main__':
    app.run()
