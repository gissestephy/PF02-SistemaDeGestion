import requests

URL = "http://127.0.0.1:5000"
sesion = requests.Session()


def registrar():
    print("\n--- REGISTRO DE USUARIO ---\n")

    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ")

    if not usuario or not contraseña:
        print("\n⚠️  Completá el usuario y la contraseña para registrarte.\n")
        return

    try:
        respuesta = sesion.post(
            f"{URL}/registro",
            json={"usuario": usuario, "contraseña": contraseña}
        )

        datos = respuesta.json()

        if respuesta.status_code == 201:
            print(f"\n  ¡Hola, {usuario}!")
            print("\n   Tu usuario se ha registrado correctamente.\n")
            print("   Ya podés iniciar sesión para consultar las tareas.\n")

        elif respuesta.status_code == 409:
            print("\n⚠️  Ese nombre de usuario ya está registrado.\n")
            print("   Intentá nuevamente con otro nombre de usuario.\n")

        elif respuesta.status_code == 400:
            print("\n⚠️  No se pudo completar el registro.\n")
            print("   Verificá que hayas ingresado correctamente los datos.\n")

        else:
            print("\n❌  Ocurrió un error al intentar registrarte.\n")
            print(f"   {datos.get('error', f'Código HTTP: {respuesta.status_code}')}\n")

    except requests.ConnectionError:
        print("\n❌  No se pudo conectar con el servidor.\n")
        print("   Verificá que el servidor Flask esté en funcionamiento.\n")

    except requests.RequestException:
        print("\n❌  Ocurrió un problema al enviar la solicitud.\n")

    except ValueError:
        print("\n❌  El servidor devolvió una respuesta que no es válida.\n")


def iniciar_sesion():
    print("\n--- INICIO DE SESIÓN ---\n")

    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ")

    if not usuario or not contraseña:
        print("\n⚠️  Ingresá tu usuario y contraseña para continuar.\n")
        return

    try:
        respuesta = sesion.post(
            f"{URL}/login",
            json={"usuario": usuario, "contraseña": contraseña}
        )

        datos = respuesta.json()

        if respuesta.status_code == 200:
            print(f"\n  ¡Bienvenido/a, {usuario}!")
            print("\n✓  Inicio de sesión exitoso.\n")
            print("   Ya podés consultar tus tareas.\n")

        elif respuesta.status_code in (401, 403):
            print("\n❌  Usuario o contraseña incorrectos.\n")
            print("   Ingresá nuevamente tus datos e intentá otra vez.\n")

        elif respuesta.status_code == 400:
            print("\n⚠️  No se pudo iniciar sesión.\n")
            print("   Verificá que hayas ingresado los datos correctamente.\n")

        else:
            print("\n❌  Ocurrió un error al iniciar sesión.\n")
            print(f"   {datos.get('error', f'Código HTTP: {respuesta.status_code}')}\n")

    except requests.ConnectionError:
        print("\n❌  No se pudo conectar con el servidor.\n")
        print("   Verificá que el servidor Flask esté en funcionamiento.\n")

    except requests.RequestException:
        print("\n❌  Ocurrió un problema al enviar la solicitud.\n")

    except ValueError:
        print("\n❌  El servidor devolvió una respuesta que no es válida.\n")


def consultar_tareas():
    print("\n--- CONSULTA DE TAREAS ---\n")

    try:
        respuesta = sesion.get(
            f"{URL}/mis-tareas",
            allow_redirects=False
        )

        if respuesta.status_code == 200:
            print("\n✓  Tareas obtenidas correctamente.\n")
            print("====================================")
            print("       MIS TAREAS - DEVTASKS")
            print("====================================\n")

            print("   Las tareas están disponibles en la interfaz web.\n")
            print(f"   {URL}/mis-tareas\n")
            print("   Abrí esa dirección en el navegador para verlas")
            print("   con su diseño completo.\n")

        elif respuesta.status_code in (301, 302, 303):
            print("\n⚠️  No tenés una sesión iniciada.\n")
            print("   Iniciá sesión antes de consultar tus tareas.\n")

        elif respuesta.status_code in (401, 403):
            print("\n❌  No tenés autorización para consultar las tareas.\n")
            print("   Iniciá sesión e intentá nuevamente.\n")

        else:
            print("\n❌  No se pudieron consultar las tareas.\n")
            print(f"   Código HTTP: {respuesta.status_code}\n")

    except requests.ConnectionError:
        print("\n❌  No se pudo conectar con el servidor.\n")
        print("   Verificá que Flask esté en funcionamiento.\n")

    except requests.RequestException:
        print("\n❌  Ocurrió un problema al consultar las tareas.\n")


def cerrar_sesion():
    print("\n--- CIERRE DE SESIÓN ---\n")

    try:
        respuesta = sesion.post(
            f"{URL}/logout",
            allow_redirects=False
        )

        if respuesta.status_code in (200, 302, 303):
            print("\n✓  Cerraste sesión correctamente.\n")
            print("  ¡Hasta la próxima!\n")

        else:
            print("\n⚠️  No se pudo confirmar el cierre de sesión.\n")
            print(f"   Código HTTP: {respuesta.status_code}\n")

    except requests.ConnectionError:
        print("\n❌  No se pudo conectar con el servidor.\n")
        print("   No fue posible confirmar el cierre de sesión.\n")

    except requests.RequestException:
        print("\n❌  Ocurrió un problema al cerrar la sesión.\n")

    finally:
        sesion.cookies.clear()


def menu():
    while True:
        print("""
========== DEVTASKS ==========

   1. Registrar usuario

   2. Iniciar sesión

   3. Consultar tareas

   4. Cerrar sesión

   0. Salir

==============================
""")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar()

        elif opcion == "2":
            iniciar_sesion()

        elif opcion == "3":
            consultar_tareas()

        elif opcion == "4":
            cerrar_sesion()

        elif opcion == "0":
            print("\n  ¡Gracias por utilizar DevTasks!\n")
            print("   Hasta la próxima.\n")
            break

        else:
            print("\n⚠️  Opción inválida. Elegí una opción del menú.\n")


if __name__ == "__main__":
    menu()