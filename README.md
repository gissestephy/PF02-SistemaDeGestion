# 🚀 Sistema de Gestión de Tareas — PFO 2

## 🌐 Proyecto

API REST desarrollada como parte del **PFO 2 — Sistema de Gestión de Tareas con API y Base de Datos**.

El proyecto implementa una API utilizando **Flask**, con persistencia de usuarios mediante **SQLite** y almacenamiento seguro de contraseñas mediante **hashing**.

La aplicación permite registrar usuarios, iniciar sesión y acceder a un recurso de tareas mediante distintos endpoints HTTP.

---

## 📌 Descripción

El objetivo del proyecto es desarrollar una API web aplicando conceptos fundamentales de desarrollo backend:

- 🌐 Creación de una API REST con Flask.
- 📦 Recepción y envío de datos en formato JSON.
- 📝 Registro de usuarios.
- 🔐 Inicio de sesión.
- 🗄️ Persistencia de datos mediante SQLite.
- 🔒 Hashing seguro de contraseñas.
- 📊 Manejo de códigos de estado HTTP.
- 🧪 Pruebas de endpoints mediante Postman.
- 🌱 Control de versiones utilizando Git y GitHub.

---

## 🎯 Objetivos

Los principales objetivos del proyecto son:

- Implementar una API REST utilizando Flask.
- Crear endpoints para el registro y autenticación de usuarios.
- Utilizar JSON como formato de intercambio de información.
- Incorporar persistencia mediante una base de datos SQLite.
- Implementar hashing para el almacenamiento seguro de contraseñas.
- Aplicar códigos de estado HTTP adecuados según cada situación.
- Realizar pruebas funcionales de los endpoints.
- Utilizar Git y GitHub para el control de versiones.

---

# 🛠️ Tecnologías Utilizadas

## 🐍 Backend

| Tecnología | Utilización |
|---|---|
| Python | Lenguaje de programación principal |
| Flask | Framework utilizado para desarrollar la API |
| Werkzeug Security | Hashing y verificación de contraseñas |
| SQLite | Persistencia de datos |

## 🧰 Herramientas

| Herramienta | Utilización |
|---|---|
| Visual Studio Code | Entorno de desarrollo |
| Postman | Prueba de los endpoints |
| DB Browser for SQLite | Visualización y comprobación de la base de datos |
| Git | Control de versiones |
| GitHub | Repositorio del proyecto |

---

# 📁 Estructura del Proyecto

```text
PFO2/
│
├── 📄 servidor.py
├── 📄 requirements.txt
├── 📄 .gitignore
└── 📄 README.md
```

Los archivos generados durante la ejecución y el desarrollo local, como `venv/`, `tareas.db`, `__pycache__/` y los archivos `.pyc`, se encuentran excluidos mediante `.gitignore`.

---

# ⚙️ Requisitos

Para ejecutar el proyecto se requiere:

- 🐍 Python 3
- 💻 Visual Studio Code
- 🌱 Git
- 📮 Postman para realizar las pruebas

SQLite se utiliza mediante el módulo `sqlite3`, incluido en Python, por lo que no requiere una instalación adicional.

---

# 🚀 Instalación y Ejecución

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/gissestephy/PF02-SistemaDeGestion.git
```

Ingresar al directorio del proyecto:

```bash
cd PFO2
```

---

## 2️⃣ Crear el entorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

---

## 3️⃣ Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Ejecutar la aplicación

Iniciar el servidor Flask mediante:

```bash
python servidor.py
```

La aplicación quedará disponible localmente en:

```text
http://127.0.0.1:5000
```

La base de datos SQLite se genera automáticamente durante la ejecución de la aplicación.

---

# 🧪 Pruebas de la API

Las pruebas funcionales de la API fueron realizadas utilizando **Postman**.

---

# 📝 Registro de Usuario

## Endpoint

```text
POST /registro
```

## URL

```text
http://127.0.0.1:5000/registro
```

## Body

En Postman se utiliza:

```text
Body → raw → JSON
```

con el siguiente contenido:

```json
{
    "usuario": "nombre",
    "contraseña": "1234"
}
```

## ✅ Registro exitoso

Cuando el usuario no existe previamente, la API devuelve:

**HTTP 201 — Created**

```json
{
    "mensaje": "Usuario registrado correctamente"
}
```

---

# ⚠️ Registro de Usuario Existente

Si se intenta registrar nuevamente un usuario que ya existe, la API devuelve:

**HTTP 409 — Conflict**

```json
{
    "error": "El usuario ya existe"
}
```

Esta respuesta permite comprobar que el nombre de usuario se encuentra configurado como único en la base de datos.

---

# 🔐 Inicio de Sesión

## Endpoint

```text
POST /login
```

## URL

```text
http://127.0.0.1:5000/login
```

## Body

```json
{
    "usuario": "nombre",
    "contraseña": "1234"
}
```

## ✅ Login exitoso

Cuando las credenciales son correctas, la API devuelve:

**HTTP 200 — OK**

```json
{
    "mensaje": "Inicio de sesión exitoso"
}
```

## ❌ Credenciales incorrectas

Cuando las credenciales no son válidas:

**HTTP 401 — Unauthorized**

```json
{
    "error": "Usuario o contraseña incorrectos"
}
```

---

# 📋 Consulta de Tareas

## Endpoint

```text
GET /tareas
```

## URL

```text
http://127.0.0.1:5000/tareas
```

El endpoint devuelve una página HTML correspondiente al sistema de gestión de tareas.

La respuesta incluye un mensaje de bienvenida y una lista de tareas de ejemplo.

---

# 🏠 Endpoint Inicial

## Endpoint

```text
GET /
```

## URL

```text
http://127.0.0.1:5000/
```

Este endpoint permite comprobar que el servidor Flask se encuentra funcionando correctamente.

---

# 🗄️ Persistencia con SQLite

La aplicación utiliza **SQLite** para almacenar los usuarios registrados.

La base de datos utilizada es:

```text
tareas.db
```

La tabla principal es:

```text
usuarios
```

## 📊 Estructura de la tabla

| Campo | Tipo | Restricciones |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `usuario` | TEXT | UNIQUE, NOT NULL |
| `contraseña` | TEXT | NOT NULL |

La restricción `UNIQUE` permite evitar el registro de dos usuarios con el mismo nombre.

---

# 🔐 Seguridad

Las contraseñas **no se almacenan en texto plano**.

Para generar el hash de la contraseña durante el registro se utiliza:

```python
generate_password_hash()
```

Para verificar la contraseña durante el inicio de sesión se utiliza:

```python
check_password_hash()
```

Por ejemplo, si el usuario ingresa:

```text
1234
```

la contraseña no se almacena directamente en la base de datos.

En su lugar, se almacena una representación hasheada similar a:

```text
scrypt:32768:8:1$...
```

Esto permite comprobar las credenciales sin almacenar la contraseña original.

---

# 📊 Códigos de Estado HTTP

| Código | Significado | Situación |
|---|---|---|
| `200` | OK | Login exitoso / consulta correcta |
| `201` | Created | Usuario registrado correctamente |
| `400` | Bad Request | Datos obligatorios faltantes |
| `401` | Unauthorized | Credenciales incorrectas |
| `409` | Conflict | Usuario ya existente |

---

# 📸 Capturas de Pruebas Exitosas

Las siguientes capturas documentan las pruebas realizadas durante la ejecución del proyecto.

## 📝 Registro exitoso

Prueba del endpoint:

```text
POST /registro
```

Resultado esperado:

```text
201 Created
```

📷 **Captura de Postman:**

<img width="1915" height="1031" alt="Captura de pantalla 2026-10-04 155234" src="https://github.com/user-attachments/assets/baaa17bb-1c4e-4a8f-9c0e-33393965f4ae" />

---

## 🔐 Login exitoso

Prueba del endpoint:

```text
POST /login
```

utilizando credenciales válidas.

Resultado esperado:

```text
200 OK
```

📷 **Captura de Postman:**

<img width="1919" height="1030" alt="Captura de pantalla 2026-10-04 160559" src="https://github.com/user-attachments/assets/b0db3452-be36-4afb-8e03-c8252df6ac71" />

---

## ⚠️ Usuario duplicado

Prueba de registro de un usuario que ya se encontraba almacenado.

Resultado:

```text
409 Conflict
```

📷 **Captura de Postman:**

<img width="1919" height="1030" alt="Captura de pantalla 2026-10-04 161212" src="https://github.com/user-attachments/assets/4a6df3ac-e8cd-42cb-9fac-dca192f58a76" />

---

## ⚠️ Usuario incorrecto

Prueba de registro de un usuario se ha ingresado incorrectamente.

Resultado:

```text
401 Unauthorized
```

📷 **Captura de Postman:**

<img width="1919" height="1030" alt="Captura de pantalla 2026-10-04 160846" src="https://github.com/user-attachments/assets/3f229c61-cf9c-49c4-86d2-d2e46af4db9d" />

---


## ⚠️ Contraseña incorrecta

Prueba de registro de que la contraseña se ha ingresado incorrectamente.

Resultado:

```text
401 Unauthorized
```

📷 **Captura de Postman:**

<img width="1919" height="1029" alt="Captura de pantalla 2026-10-04 160833" src="https://github.com/user-attachments/assets/dbf2fbff-3b03-4dff-8b19-a4623b0c9c13" />

---

## 🗄️ Base de Datos

Verificación de la tabla `usuarios` mediante **DB Browser for SQLite**.

Se comprobó:

- La existencia de la tabla.
- El usuario registrado.
- La persistencia de los datos.
- El almacenamiento de la contraseña mediante hash.

📷 **Captura de DB Browser for SQLite:**

<img width="1919" height="1030" alt="Captura de pantalla 2026-10-04 160528" src="https://github.com/user-attachments/assets/64052e2d-30be-4b5a-83e9-cf68c7b9b0b9" />


---

## 📋 Endpoint `/tareas`

Prueba del endpoint:

```text
GET /tareas
```

Resultado:

```text
200 OK
```

📷 **Captura del navegador:**

<img width="1919" height="1027" alt="Captura de pantalla 2026-10-04 155301" src="https://github.com/user-attachments/assets/1df9669e-b134-4a28-81b8-29ddaf2864d2" />

---

## Vista del Navegador

📷 **Captura del navegador:**

<img width="1627" height="922" alt="image" src="https://github.com/user-attachments/assets/e4babf8c-32ca-4bcf-a91d-dd89744a6060" />


# 🧠 Fundamentación

## 🔒 ¿Por qué utilizar hashing para las contraseñas?

Las contraseñas no deberían almacenarse directamente en una base de datos debido al riesgo que esto representa ante una posible exposición de la información.

El hashing permite almacenar una representación derivada de la contraseña y posteriormente verificar las credenciales ingresadas sin necesidad de conservar la contraseña original en texto plano.

En este proyecto se utilizan las funciones `generate_password_hash()` y `check_password_hash()` proporcionadas por Werkzeug Security.

---

## 🗄️ ¿Por qué utilizar SQLite?

SQLite es una base de datos liviana y sencilla de integrar con Python.

Una de sus principales características es que no requiere un servidor de base de datos independiente, ya que la información se almacena en un archivo.

Para el alcance de este proyecto, SQLite permite implementar persistencia de datos de manera sencilla y adecuada.

---

# 🌱 Control de Versiones

El proyecto utiliza **Git** para el control de versiones y **GitHub** como repositorio remoto.

Los archivos principales del repositorio son:

```text
.gitignore
README.md
requirements.txt
servidor.py
```

El archivo `.gitignore` evita incorporar al repositorio archivos generados localmente:

```gitignore
venv/
tareas.db
__pycache__/
*.pyc
```

De esta manera, el repositorio contiene únicamente los archivos necesarios para el desarrollo y documentación del proyecto.

---

# 📚 Conclusión

El desarrollo del proyecto permitió implementar una API REST utilizando Flask e integrar diferentes conceptos de programación backend.

Se incorporó persistencia de datos mediante SQLite, registro y autenticación de usuarios, hashing de contraseñas, intercambio de información mediante JSON y manejo de códigos de estado HTTP.

Las pruebas realizadas mediante Postman permitieron comprobar el funcionamiento de los principales endpoints, mientras que DB Browser for SQLite permitió verificar la persistencia de los usuarios y el almacenamiento seguro de las contraseñas.

Finalmente, el uso de Git y GitHub permitió aplicar herramientas de control de versiones y gestión del código fuente.

---
