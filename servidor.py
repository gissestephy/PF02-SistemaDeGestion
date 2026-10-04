import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

BASE_DATOS = "tareas.db"

def inicializar_db():
    conexion = sqlite3.connect(BASE_DATOS)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

@app.route("/")
def inicio():
    return "<h1>Sistema de Gestión de Tareas</h1>"

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    contraseña_hash = generate_password_hash(contraseña)

    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )

        conexion.commit()

    except sqlite3.IntegrityError:
        conexion.close()
        return jsonify({"error": "El usuario ya existe"}), 409

    conexion.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT contraseña FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado is None:
        return jsonify({
            "error": "Usuario o contraseña incorrectos"
        }), 401

    contraseña_hash = resultado[0]

    if check_password_hash(contraseña_hash, contraseña):
        return jsonify({
            "mensaje": "Inicio de sesión exitoso"
        }), 200

    return jsonify({
        "error": "Usuario o contraseña incorrectos"
    }), 401

@app.route("/tareas", methods=["GET"])
def tareas():
    return """
    <html>
        <head>
            <title>Sistema de Gestión de Tareas</title>
        </head>
        <body>
            <h1>¡Bienvenido al Sistema de Gestión de Tareas!</h1>
            <p>La API Flask está funcionando correctamente.</p>

            <h2>Tareas</h2>

            <ul>
                <li>Estudiar Flask</li>
                <li>Practicar SQLite</li>
                <li>Probar la API</li>
            </ul>
        </body>
    </html>
    """

if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True)