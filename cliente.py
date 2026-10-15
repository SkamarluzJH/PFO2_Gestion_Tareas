import requests

BASE = "http://127.0.0.1:5000"
sesion = requests.Session()  


def pedir_datos():
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()
    return {"usuario": usuario, "contraseña": contraseña}


def mostrar(resp):
    try:
        print(f"[{resp.status_code}]", resp.json())
    except ValueError:
        print(f"[{resp.status_code}]\n{resp.text}")


def main():
    while True:
        print("\n1) Registrarse  2) Iniciar sesión  3) Ver tareas  4) Salir")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                mostrar(sesion.post(f"{BASE}/registro", json=pedir_datos()))
            elif op == "2":
                mostrar(sesion.post(f"{BASE}/login", json=pedir_datos()))
            elif op == "3":
                mostrar(sesion.get(f"{BASE}/tareas"))
            elif op == "4":
                break
            else:
                print("Opción inválida")
        except requests.ConnectionError:
            print("No se pudo conectar: ¿está corriendo servidor.py?")


if __name__ == "__main__":
    main()