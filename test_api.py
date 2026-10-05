import pytest
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


@pytest.fixture
def headers():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "clave-de-prueba"})
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


def crear_gasto(headers, categoria, importe, fecha="2026-09-10"):
    return client.post(
        "/gastos",
        json={"categoria": categoria, "importe": importe, "fecha": fecha},
        headers=headers,
    )


def test_raiz_responde_bienvenida():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Bienvenido a expense-tracker API"}


def test_login_correcto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "clave-de-prueba"})
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()


def test_login_incorrecto():
    respuesta = client.post("/login", json={"usuario": "bosco", "password": "mala"})
    assert respuesta.status_code == 401


def test_gastos_sin_token():
    assert client.get("/gastos").status_code == 401


def test_crear_gasto_sin_token():
    respuesta = client.post(
        "/gastos", json={"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
    )
    assert respuesta.status_code == 401


def test_gastos_con_token_invalido(headers):
    token = headers["Authorization"].removeprefix("Bearer ")
    manipulado = token[:-1] + ("A" if token[-1] != "A" else "B")
    respuesta = client.get("/gastos", headers={"Authorization": f"Bearer {manipulado}"})
    assert respuesta.status_code == 401


def test_crear_gasto_se_guarda_en_bd(headers):
    respuesta = crear_gasto(headers, "comida", 10.5)
    assert respuesta.status_code == 201
    assert respuesta.json()["categoria"] == "comida"

    lista = client.get("/gastos", headers=headers)
    assert lista.status_code == 200
    assert len(lista.json()) == 1
    assert lista.json()[0]["importe"] == 10.5


@pytest.mark.parametrize("categoria,importe,fecha", [
    ("123", 10.0, "2026-09-10"),
    ("comida", -5.0, "2026-09-10"),
    ("comida", 10.0, "fecha-mala"),
])
def test_gasto_invalido_da_400_y_no_se_guarda(headers, categoria, importe, fecha):
    respuesta = crear_gasto(headers, categoria, importe, fecha)
    assert respuesta.status_code == 400
    assert client.get("/gastos", headers=headers).json() == []


@pytest.mark.parametrize("cuerpo", [
    {"categoria": "comida", "importe": "abc", "fecha": "2026-09-10"},
    {"categoria": "comida", "fecha": "2026-09-10"},
])
def test_cuerpo_mal_formado_da_422(headers, cuerpo):
    respuesta = client.post("/gastos", json=cuerpo, headers=headers)
    assert respuesta.status_code == 422


def test_filtrar_por_categoria_excluye_las_demas(headers):
    crear_gasto(headers, "comida", 2.0)
    crear_gasto(headers, "ocio", 7.0)

    respuesta = client.get("/gastos?categoria=comida", headers=headers)
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["categoria"] == "comida"


def test_totales(headers):
    crear_gasto(headers, "comida", 10.0)
    crear_gasto(headers, "ocio", 5.0)

    respuesta = client.get("/gastos/total", headers=headers)
    assert respuesta.status_code == 200
    assert respuesta.json()["total_general"] == 15.0
    assert respuesta.json()["por_categoria"] == {"comida": 10.0, "ocio": 5.0}


def test_totales_con_tabla_vacia(headers):
    respuesta = client.get("/gastos/total", headers=headers)
    assert respuesta.status_code == 200
    assert respuesta.json()["total_general"] == 0
    assert respuesta.json()["por_categoria"] == {}
    
    


