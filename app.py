from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.getenv("DATA_DIR", "/app/data")
DATABASE = os.path.join(DATA_DIR, "notas.db")


def inicializar_banco():
    os.makedirs(DATA_DIR, exist_ok=True)

    conexao = sqlite3.connect(DATABASE)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/notas", methods=["POST"])
def criar_nota():
    dados = request.get_json()

    if not dados or "texto" not in dados:
        return jsonify({"erro": "O campo 'texto' é obrigatório"}), 400

    texto = dados["texto"]

    conexao = sqlite3.connect(DATABASE)

    data_hora = datetime.now().isoformat()

    cursor = conexao.execute(
        "INSERT INTO notas (texto, data_hora) VALUES (?, ?)",
        (texto, data_hora)
    )

    conexao.commit()

    nota_id = cursor.lastrowid

    conexao.close()

    return jsonify({
        "id": nota_id,
        "texto": texto,
        "data_hora": data_hora
    }), 201


@app.route("/notas", methods=["GET"])
def listar_notas():
    conexao = sqlite3.connect(DATABASE)

    cursor = conexao.execute(
        "SELECT id, texto, data_hora FROM notas ORDER BY id"
    )

    notas = []

    for linha in cursor.fetchall():
        notas.append({
            "id": linha[0],
            "texto": linha[1],
            "data_hora": linha[2]
        })

    conexao.close()

    return jsonify(notas)


inicializar_banco()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
