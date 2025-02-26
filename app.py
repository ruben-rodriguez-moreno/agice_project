from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sqlite3
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

DATABASE = 'agice.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/guardar_documento', methods=['POST'])
def guardar_documento():
    data = request.get_json()
    titulo = data.get('titulo')
    contenido = data.get('contenido')
    if not titulo or not contenido:
        return jsonify({"error": "Falta título o contenido"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO documentos (titulo, contenido) VALUES (?, ?)', (titulo, contenido))
    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()
    return jsonify({"mensaje": "Documento guardado", "id": doc_id}), 201

@app.route('/obtener_documento/<int:doc_id>', methods=['GET'])
def obtener_documento(doc_id):
    conn = get_db_connection()
    documento = conn.execute('SELECT * FROM documentos WHERE id = ?', (doc_id,)).fetchone()
    conn.close()
    if documento is None:
        return jsonify({"error": "Documento no encontrado"}), 404
    return jsonify(dict(documento))

if __name__ == '__main__':
    app.run(debug=True)
