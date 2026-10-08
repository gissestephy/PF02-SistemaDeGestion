
import os
import sqlite3
from html import escape

from flask import (
    Flask,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    render_template_string
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

# Clave para las sesiones de Flask.
# Para producción, configurá FLASK_SECRET_KEY como variable de entorno.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "clave-local-solo-para-desarrollo"
)

BASE_DATOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tareas.db"
)


# ==================================================
# BASE DE DATOS SQLITE
# ==================================================

def conectar_db():
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_db():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def crear_usuario(usuario, contraseña):
    contraseña_hash = generate_password_hash(contraseña)
    conexion = conectar_db()

    try:
        conexion.execute(
            """
            INSERT INTO usuarios (usuario, contraseña)
            VALUES (?, ?)
            """,
            (usuario, contraseña_hash)
        )

        conexion.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conexion.close()


def verificar_usuario(usuario, contraseña):
    conexion = conectar_db()

    try:
        resultado = conexion.execute(
            """
            SELECT id, usuario, contraseña
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,)
        ).fetchone()

        if resultado and check_password_hash(
            resultado["contraseña"], contraseña
        ):
            return {
                "id": resultado["id"],
                "usuario": resultado["usuario"]
            }

        return None

    finally:
        conexion.close()


# ==================================================
# TAREAS FICTICIAS DE DESARROLLO DE SOFTWARE
# ==================================================

TAREAS = [
    {
        "materia": "Programación I",
        "titulo": "Desarrollar una calculadora en Python",
        "detalle": (
            "Practicar variables, funciones y estructuras de control."
        ),
        "fecha": "15/10/2026",
        "estado": "Pendiente"
    },
    {
        "materia": "Bases de Datos",
        "titulo": "Diseñar una base de datos para una biblioteca",
        "detalle": (
            "Crear tablas, definir claves y realizar consultas SQL."
        ),
        "fecha": "19/10/2026",
        "estado": "En curso"
    },
    {
        "materia": "Programación Web",
        "titulo": "Crear una página web con HTML y CSS",
        "detalle": (
            "Diseñar una interfaz adaptable a diferentes pantallas."
        ),
        "fecha": "23/10/2026",
        "estado": "Pendiente"
    },
    {
        "materia": "Redes y Sistemas",
        "titulo": "Investigar el modelo cliente-servidor",
        "detalle": (
            "Explicar el funcionamiento de TCP, HTTP y las API."
        ),
        "fecha": "27/10/2026",
        "estado": "Pendiente"
    },
    {
        "materia": "Ingeniería de Software",
        "titulo": "Documentar un proyecto de software",
        "detalle": (
            "Preparar requisitos, objetivos y casos de prueba."
        ),
        "fecha": "30/10/2026",
        "estado": "Completada"
    }
]


# ==================================================
# ESTILOS DE LA PÁGINA WEB
# ==================================================

ESTILOS = """
<style>
:root {
    --fondo: #f4f6fc;
    --texto: #202642;
    --secundario: #727b96;
    --primario: #6558df;
    --borde: #e7e9f2;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: var(--fondo);
    color: var(--texto);
}

nav {
    background: white;
    border-bottom: 1px solid var(--borde);
    padding: 17px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.logo {
    color: var(--primario);
    font-size: 22px;
    font-weight: 800;
    text-decoration: none;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.nav-links form {
    margin: 0;
}

a {
    text-decoration: none;
    color: inherit;
}

button,
.boton {
    border: 0;
    border-radius: 10px;
    padding: 12px 17px;
    font: inherit;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: inline-block;
    text-align: center;
}

.boton-principal {
    background: var(--primario);
    color: white;
}

.boton-secundario {
    background: #eeecff;
    color: var(--primario);
}

.boton-salir {
    background: #fff0f0;
    color: #bd4040;
}

button:hover,
.boton:hover {
    opacity: 0.86;
}

.contenedor {
    width: min(1080px, 90%);
    margin: 42px auto;
}

.hero {
    background: linear-gradient(125deg, #6558df, #8d79f4);
    color: white;
    border-radius: 24px;
    padding: 48px;
}

.etiqueta {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border-radius: 30px;
    padding: 8px 13px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 46px);
    line-height: 1.15;
    max-width: 700px;
    margin: 22px 0 15px;
}

.hero p {
    color: #efedff;
    max-width: 620px;
    line-height: 1.8;
}

.hero .boton {
    margin-top: 15px;
    background: white;
    color: var(--primario);
}

.seccion-titulo {
    margin: 38px 0 20px;
}

.seccion-titulo h2 {
    margin-bottom: 8px;
}

.muted {
    color: var(--secundario);
    line-height: 1.7;
}

.tarjetas {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 18px;
}

.tarjeta {
    background: white;
    padding: 23px;
    border: 1px solid var(--borde);
    border-radius: 17px;
}

.icono {
    font-size: 28px;
    margin-bottom: 13px;
}

.tarjeta h3 {
    font-size: 17px;
    margin: 0 0 10px;
}

.formulario {
    max-width: 470px;
    margin: 45px auto;
    background: white;
    border: 1px solid var(--borde);
    border-radius: 20px;
    padding: 32px;
}

.formulario h1 {
    margin-top: 0;
}

label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    margin: 18px 0 8px;
}

input {
    width: 100%;
    padding: 13px;
    border: 1px solid #dfe2ed;
    border-radius: 9px;
    font: inherit;
}

input:focus {
    outline: 2px solid #c5beff;
    border-color: var(--primario);
}

.formulario button {
    width: 100%;
    margin-top: 22px;
}

.mensaje {
    background: #fff0f0;
    color: #a62e2e;
    border-radius: 9px;
    padding: 12px;
    margin-bottom: 15px;
}

.mensaje-ok {
    background: #eaf9ef;
    color: #217a43;
    border-radius: 9px;
    padding: 12px;
    margin-bottom: 15px;
}

.cabecera-panel {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
}

.lista-tareas {
    display: grid;
    gap: 15px;
    margin-top: 25px;
}

.tarea {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 15px;
    padding: 22px;
}

.materia {
    color: var(--primario);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.tarea h3 {
    margin: 10px 0;
}

.datos-tarea {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 17px;
}

.estado {
    padding: 7px 11px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    background: #fff3d9;
    color: #966100;
}

.estado.en-curso {
    background: #e9efff;
    color: #3659b7;
}

.estado.completada {
    background: #e4f7eb;
    color: #247847;
}

footer {
    text-align: center;
    color: var(--secundario);
    padding: 28px 15px;
    font-size: 13px;
}

@media (max-width: 600px) {
    nav {
        padding: 16px 5%;
    }

    .contenedor {
        margin: 25px auto;
    }

    .hero {
        padding: 28px 23px;
    }

    .formulario {
        padding: 24px;
    }
}
</style>
"""


# ==================================================
# PLANTILLA HTML GENERAL
# ==================================================

def pagina(contenido, titulo="DevTasks"):
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1">

            <title>{{ titulo }}</title>
            {{ estilos|safe }}
        </head>

        <body>
            <nav>
                <a class="logo" href="/">⌘ DevTasks</a>

                <div class="nav-links">
                    {% if session.get('usuario') %}
                        <span>Hola, {{ session['usuario'] }}</span>

                        <a class="boton boton-secundario"
                           href="/mis-tareas">
                            Mis tareas
                        </a>

                        <form method="POST" action="/logout">
                            <button class="boton-salir" type="submit">
                                Cerrar sesión
                            </button>
                        </form>
                    {% else %}
                        <a class="boton boton-secundario"
                           href="/login-web">
                            Iniciar sesión
                        </a>

                        <a class="boton boton-principal"
                           href="/registro-web">
                            Registrarse
                        </a>
                    {% endif %}
                </div>
            </nav>

            {{ contenido|safe }}

            <footer>
                DevTasks · Proyecto académico ficticio ·
                Desarrollo de Software
            </footer>
        </body>
        </html>
        """,
        contenido=contenido,
        titulo=titulo,
        estilos=ESTILOS
    )


# ==================================================
# PÁGINA DE INICIO
# ==================================================

@app.route("/")
def inicio():
    contenido = """
    <main class="contenedor">
        <section class="hero">
            <span class="etiqueta">
                🎓 DESARROLLO DE SOFTWARE
            </span>

            <h1>Organizá tus ideas. Construye tu futuro</h1>

            <p>
                Tu espacio académico para organizar actividades,
                seguir tus entregas y avanzar en tu camino como
                desarrollador de software.
            </p>

            <a class="boton" href="/registro-web">
                Comenzar ahora →
            </a>
        </section>

        <section class="seccion-titulo">
            <h2>Todo tu aprendizaje, en un solo lugar</h2>

            <p class="muted">
                Una plataforma pensada para acompañarte durante la carrera.
            </p>
        </section>

        <section class="tarjetas">
            <article class="tarjeta">
                <div class="icono">💻</div>
                <h3>Programación</h3>
                <p class="muted">
                    Ejercicios, algoritmos y proyectos con Python.
                </p>
            </article>

            <article class="tarjeta">
                <div class="icono">🗄️</div>
                <h3>Bases de datos</h3>
                <p class="muted">
                    Consultas SQL, tablas y almacenamiento.
                </p>
            </article>

            <article class="tarjeta">
                <div class="icono">🌐</div>
                <h3>Desarrollo web</h3>
                <p class="muted">
                    HTML, CSS, API REST y aplicaciones web.
                </p>
            </article>
        </section>
    </main>
    """

    return pagina(contenido, "Inicio | DevTasks")


# ==================================================
# REGISTRO DE USUARIOS: API REST
# ==================================================

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON válido"
        }), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contraseña, str):
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    usuario = usuario.strip()

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    if len(usuario) > 50 or len(contraseña) > 128:
        return jsonify({
            "error": "El usuario o la contraseña son demasiado largos"
        }), 400

    if crear_usuario(usuario, contraseña):
        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    return jsonify({
        "error": "El usuario ya existe"
    }), 409


# ==================================================
# REGISTRO DESDE LA WEB
# ==================================================

@app.route("/registro-web", methods=["GET", "POST"])
def registro_web():
    error = ""

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "")

        if not usuario or not contraseña:
            error = "Completá todos los campos."

        elif len(usuario) > 50 or len(contraseña) > 128:
            error = "El usuario o la contraseña son demasiado largos."

        elif crear_usuario(usuario, contraseña):
            return redirect(url_for("login_web", registrado="1"))

        else:
            error = "Ese nombre de usuario ya está registrado."

    contenido = """
    <main class="contenedor">
        <section class="formulario">
            <h1>Crear una cuenta</h1>

            <p class="muted">
                Registrate para acceder a tus actividades académicas.
            </p>

            {% if error %}
                <div class="mensaje">{{ error }}</div>
            {% endif %}

            <form method="POST">
                <label for="usuario">Nombre de usuario</label>
                <input id="usuario" name="usuario"
                       maxlength="50" autocomplete="username" required>

                <label for="contraseña">Contraseña</label>
                <input id="contraseña" name="contraseña"
                       type="password" maxlength="128"
                       autocomplete="new-password" required>

                <button class="boton-principal" type="submit">
                    Crear cuenta
                </button>
            </form>

            <p class="muted">
                ¿Ya tenés cuenta?
                <a href="/login-web">Iniciá sesión</a>.
            </p>
        </section>
    </main>
    """

    return pagina(
        render_template_string(contenido, error=error),
        "Registro | DevTasks"
    )


# ==================================================
# INICIO DE SESIÓN: API REST
# ==================================================

@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON válido"
        }), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contraseña, str):
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    usuario = usuario.strip()

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    resultado = verificar_usuario(usuario, contraseña)

    if resultado is None:
        return jsonify({
            "error": "Usuario o contraseña incorrectos"
        }), 401

    session.clear()
    session["usuario"] = resultado["usuario"]
    session["usuario_id"] = resultado["id"]

    return jsonify({
        "mensaje": "Inicio de sesión exitoso"
    }), 200


# ==================================================
# INICIO DE SESIÓN DESDE LA WEB
# ==================================================

@app.route("/login-web", methods=["GET", "POST"])
def login_web():
    error = ""
    registrado = request.args.get("registrado") == "1"

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "")

        resultado = None

        if usuario and contraseña:
            resultado = verificar_usuario(usuario, contraseña)

        if resultado:
            session.clear()
            session["usuario"] = resultado["usuario"]
            session["usuario_id"] = resultado["id"]

            return redirect(url_for("tareas"))

        error = "Usuario o contraseña incorrectos."

    contenido = """
    <main class="contenedor">
        <section class="formulario">
            <h1>¡Qué bueno verte!</h1>

            <p class="muted">
                Ingresá a tu espacio de Desarrollo de Software.
            </p>

            {% if registrado %}
                <div class="mensaje-ok">
                    Cuenta creada correctamente.
                    Ya podés iniciar sesión.
                </div>
            {% endif %}

            {% if error %}
                <div class="mensaje">{{ error }}</div>
            {% endif %}

            <form method="POST">
                <label for="usuario">Nombre de usuario</label>
                <input id="usuario" name="usuario"
                       autocomplete="username" required>

                <label for="contraseña">Contraseña</label>
                <input id="contraseña" name="contraseña"
                       type="password"
                       autocomplete="current-password" required>

                <button class="boton-principal" type="submit">
                    Iniciar sesión
                </button>
            </form>

            <p class="muted">
                ¿Sos nuevo?
                <a href="/registro-web">Creá tu cuenta</a>.
            </p>
        </section>
    </main>
    """

    return pagina(
        render_template_string(
            contenido,
            error=error,
            registrado=registrado
        ),
        "Iniciar sesión | DevTasks"
    )


# ==================================================
# PÁGINA HTML DE BIENVENIDA: GET /tareas
# ==================================================

@app.route("/tareas", methods=["GET"])
def tareas():
    # La consigna pide que este endpoint muestre una
    # página HTML de bienvenida.
    contenido = """
    <main class="contenedor">
        <section class="hero">
            <span class="etiqueta">
                🎓 DESARROLLO DE SOFTWARE
            </span>

            <h1>¡Bienvenido al Sistema de Gestión de Tareas!</h1>

            <p>
                Un espacio académico para organizar actividades,
                practicar programación y seguir aprendiendo
                desarrollo de software.
            </p>

            <a class="boton" href="/registro-web">
                Crear una cuenta →
            </a>

            <a class="boton"
               style="margin-left:8px"
               href="/login-web">
                Iniciar sesión
            </a>
        </section>

        <section class="seccion-titulo">
            <h2>¿Qué vas a encontrar?</h2>

            <p class="muted">
                Actividades ficticias relacionadas con las materias
                de la carrera.
            </p>
        </section>

        <section class="tarjetas">
            <article class="tarjeta">
                <div class="icono">💻</div>
                <h3>Programación</h3>
                <p class="muted">
                    Ejercicios de Python, algoritmos y resolución
                    de problemas.
                </p>
            </article>

            <article class="tarjeta">
                <div class="icono">🗄️</div>
                <h3>Bases de datos</h3>
                <p class="muted">
                    Prácticas de SQL, tablas y almacenamiento
                    de información.
                </p>
            </article>

            <article class="tarjeta">
                <div class="icono">🌐</div>
                <h3>Desarrollo web</h3>
                <p class="muted">
                    Creación de páginas web y desarrollo de API REST.
                </p>
            </article>
        </section>

        <section class="seccion-titulo">
            <h2>Actividades de ejemplo</h2>
            <p class="muted">
                Estas tareas son ficticias y sirven como muestra
                del contenido académico.
            </p>
        </section>

        <section class="lista-tareas">
            <article class="tarea">
                <span class="materia">Programación I</span>
                <h3>Desarrollar una calculadora en Python</h3>
                <p class="muted">
                    Practicar funciones, variables y estructuras de control.
                </p>
                <span class="estado">Pendiente</span>
            </article>

            <article class="tarea">
                <span class="materia">Bases de Datos</span>
                <h3>Diseñar una base de datos para una biblioteca</h3>
                <p class="muted">
                    Crear tablas y realizar consultas SQL.
                </p>
                <span class="estado en-curso">En curso</span>
            </article>

            <article class="tarea">
                <span class="materia">Programación Web</span>
                <h3>Crear una página con HTML y CSS</h3>
                <p class="muted">
                    Diseñar una interfaz adaptable a distintas pantallas.
                </p>
                <span class="estado">Pendiente</span>
            </article>
        </section>
    </main>
    """

    return pagina(contenido, "Bienvenida | DevTasks")


# ==================================================
# PANEL DE TAREAS: REQUIERE INICIAR SESIÓN
# ==================================================

@app.route("/mis-tareas", methods=["GET"])
def mis_tareas():
    if not session.get("usuario_id"):
        return redirect(url_for("login_web"))

    tarjetas = ""

    for tarea in TAREAS:
        estado = tarea["estado"]

        clase = {
            "Pendiente": "",
            "En curso": "en-curso",
            "Completada": "completada"
        }.get(estado, "")

        tarjetas += f"""
        <article class="tarea">
            <span class="materia">{escape(tarea['materia'])}</span>

            <h3>{escape(tarea['titulo'])}</h3>

            <p class="muted">{escape(tarea['detalle'])}</p>

            <div class="datos-tarea">
                <span class="muted">
                    📅 Entrega: {escape(tarea['fecha'])}
                </span>

                <span class="estado {clase}">
                    {escape(estado)}
                </span>
            </div>
        </article>
        """

    total = len(TAREAS)
    completadas = sum(
        tarea["estado"] == "Completada"
        for tarea in TAREAS
    )
    por_finalizar = total - completadas

    contenido = f"""
    <main class="contenedor">
        <section class="cabecera-panel">
            <div>
                <p class="materia">PANEL ACADÉMICO</p>
                <h1>Mis tareas</h1>
                <p class="muted">
                    ¡Hola, {escape(session['usuario'])}!
                    Estas son tus actividades de ejemplo.
                </p>
            </div>

            <a class="boton boton-secundario" href="/tareas">
                Página de bienvenida
            </a>
        </section>

        <section class="tarjetas" style="margin-top:25px">
            <article class="tarjeta">
                <div class="icono">📚</div>
                <h3>{total} actividades</h3>
                <p class="muted">Tareas ficticias de la carrera.</p>
            </article>

            <article class="tarjeta">
                <div class="icono">✅</div>
                <h3>{completadas} completadas</h3>
                <p class="muted">Actividades finalizadas.</p>
            </article>

            <article class="tarjeta">
                <div class="icono">📝</div>
                <h3>{por_finalizar} por finalizar</h3>
                <p class="muted">Pendientes o en curso.</p>
            </article>
        </section>

        <section class="lista-tareas">
            {tarjetas}
        </section>

        <p class="muted" style="margin-top:22px">
            Las actividades y fechas son ejemplos ficticios.
            No representan entregas reales ni se guardan
            como tareas individuales en SQLite.
        </p>
    </main>
    """

    return pagina(contenido, "Mis tareas | DevTasks")


# ==================================================
# CIERRE DE SESIÓN
# ==================================================

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("inicio"))


# ==================================================
# INICIO DEL SERVIDOR
# ==================================================

inicializar_db()

if __name__ == "__main__":
    app.run(debug=True)
