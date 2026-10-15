

import sqlite3
from flask import Flask, request, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cambiar-esta-clave-en-produccion"
DB = "tareas.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT UNIQUE NOT NULL,
                   password_hash TEXT NOT NULL
               )"""
        )


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contraseña = datos.get("contraseña") or ""
    if not usuario or not contraseña:
        return jsonify({"error": "Faltan 'usuario' o 'contraseña'"}), 400

    try:
        get_db().execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, generate_password_hash(contraseña)),
        )
        get_db().commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    return jsonify({"mensaje": f"Usuario '{usuario}' registrado"}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contraseña = datos.get("contraseña") or ""

    fila = get_db().execute(
        "SELECT password_hash FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    if fila is None or not check_password_hash(fila["password_hash"], contraseña):
        return jsonify({"error": "Credenciales inválidas"}), 401

    session["usuario"] = usuario
    return jsonify({"mensaje": f"Bienvenido, {usuario}"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"error": "Debés iniciar sesión primero"}), 401
    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Tareas</title></head>
<body>
  <h1>¡Bienvenido/a, {usuario}!</h1>
  <p>Este es tu sistema de gestión de tareas.</p>
</body>
</html>"""


if __name__ == "__main__":
    init_db()
    app.run(debug=True)