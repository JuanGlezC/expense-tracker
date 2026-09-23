from storage import dict_a_gasto,guardar_transacciones,cargar_transacciones
import pytest
from excepciones import DatosIncompletosError


@pytest.fixture
def diccionario_valido():
    return {
    "categoria": "ocio",
    "importe": 8.0,
    "fecha": "2026-09-12"
  }

def test_diccionario_se_crea_correctamente(diccionario_valido):
    
    
    gasto = dict_a_gasto(diccionario_valido)
    assert gasto.categoria == "ocio"
    assert gasto.importe == 8.0
    assert gasto.fecha == "2026-09-12"


def test_falta_clave_lanza_datos_incompletos_error():
    datos_incompletos = {"categoria": "comida", "importe": 10.0}  # falta "fecha"
    with pytest.raises(DatosIncompletosError):
        dict_a_gasto(datos_incompletos)

def test_guardar_y_cargar_transacciones(tmp_path):
    ruta = tmp_path / "datos.json"
    datos = [{"categoria": "ocio", "importe": 10.0, "fecha": "2026-09-10"}]
    guardar_transacciones(datos, ruta)
    resultado = cargar_transacciones(ruta)
    assert resultado == datos