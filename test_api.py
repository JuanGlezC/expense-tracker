from fastapi.testclient import TestClient
from api import app, get_gestor
from gestor import GestorGastos

client = TestClient(app)

def obtener_token(usuario="bosco", password="clave-de-prueba"):
    respuesta = client.post("/login", json={"usuario": usuario, "password": password})
    return respuesta.json()["access_token"]

def test_raiz_responde_bienvenida():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Bienvenido a expense-tracker API"}

def test_crear_gasto(tmp_path):
    ruta_prueba = tmp_path / "gastos_test.json"

    def get_gestor_prueba():
        return GestorGastos(ruta_prueba)

    app.dependency_overrides[get_gestor] = get_gestor_prueba

    token = obtener_token()
    respuesta = client.post(
        "/gastos",
        json={"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["categoria"] == "comida"

    respuesta_lista = client.get("/gastos", headers={"Authorization": f"Bearer {token}"})
    assert respuesta_lista.status_code == 200
    assert len(respuesta_lista.json()) == 1

    app.dependency_overrides.clear()


def test_login_correcto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "clave-de-prueba"})
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()

def test_login_incorrecto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "mala"})
    assert respuesta.status_code == 401