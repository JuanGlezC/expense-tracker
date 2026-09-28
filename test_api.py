from fastapi.testclient import TestClient
from api import app, get_gestor
from gestor import GestorGastos
import pytest
from excepciones import CategoriaInvalidaError,FechaInvalidaError,ImporteInvalidoError
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

@pytest.mark.parametrize("categoria,importe,fecha", [
    ("123", 10.0, "2026-09-10"),
    ("comida", -5.0, "2026-09-10"),
    ("comida", 10.0, "fecha-mala"),
])
def test_crear_gasto_datos_invalidos(categoria, importe, fecha, tmp_path):
    ruta_prueba=tmp_path / "gastos_test.json"

    def get_gestor_prueba():
        return GestorGastos(ruta_prueba)
    app.dependency_overrides[get_gestor]=get_gestor_prueba

    token=obtener_token()
    respuesta = client.post(
            "/gastos",
            json={"categoria": categoria, "importe": importe, "fecha": fecha},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert respuesta.status_code==400
    app.dependency_overrides.clear()


def test_login_correcto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "clave-de-prueba"})
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()

def test_login_incorrecto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "mala"})
    assert respuesta.status_code == 401

def test_gastos_sin_token():
    respuesta = client.get("/gastos")
    assert respuesta.status_code == 401

def test_gastos_con_token_invalido():

    token=obtener_token()
    token_manipulado = token[:-1] + ("A" if token[-1] != "A" else "B")
    respuesta = client.get(
        "/gastos",
        headers={"Authorization": f"Bearer {token_manipulado}"},
    )
    assert respuesta.status_code==401

def test_listar_gastos_filtrados_por_categoria(tmp_path):
    ruta_prueba = tmp_path / "gastos_test.json"
    def get_gestor_prueba():
            return GestorGastos(ruta_prueba)
    
    app.dependency_overrides[get_gestor] = get_gestor_prueba
    token=obtener_token()
    respuesta = client.post(
               "/gastos",
               json={"categoria": "comida", "importe": 2.0, "fecha": "2026-01-23"},
               headers={"Authorization": f"Bearer {token}"},
           )
    
    assert respuesta.status_code == 201
    
    
    respuesta_lista = client.get("/gastos?categoria=comida", headers={"Authorization": f"Bearer {token}"})
    assert respuesta_lista.status_code == 200
    
    assert len(respuesta_lista.json()) == 1
    assert respuesta_lista.json()[0]["categoria"]=="comida"

def test_obtener_total_de_gastos(tmp_path):
    ruta_prueba = tmp_path /"gastos_test.json"
    def get_gestor_prueba():
        return GestorGastos(ruta_prueba)
    app.dependency_overrides[get_gestor]=get_gestor_prueba
    token=obtener_token()
    respuesta1 = client.post(
    "/gastos",
    json={"categoria": "comida", "importe": 10.0, "fecha": "2026-01-23"},
    headers={"Authorization": f"Bearer {token}"},
)
    assert respuesta1.status_code == 201

    respuesta2 = client.post(
    "/gastos",
    json={"categoria": "ocio", "importe": 5.0, "fecha": "2026-01-24"},
    headers={"Authorization": f"Bearer {token}"},
    )
    assert respuesta2.status_code == 201
    respuesta_total = client.get("/gastos/total", headers={"Authorization": f"Bearer {token}"})
    assert respuesta_total.status_code == 200
    assert respuesta_total.json()["total_general"] == 15.0
    assert respuesta_total.json()["por_categoria"]["comida"] == 10.0
    assert respuesta_total.json()["por_categoria"]["ocio"] == 5.0
        
    
    


