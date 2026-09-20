from gasto import Gasto
from excepciones import CategoriaInvalidaError,FechaInvalidaError,ImporteInvalidoError,DatosIncompletosError
import pytest
from storage import dict_a_gasto

def test_gasto_valido_se_crea_correctamente():
    gasto = Gasto(categoria="comida", importe=15.5, fecha="2026-09-10")
    assert gasto.categoria == "comida"
    assert gasto.importe == 15.5
    assert gasto.fecha == "2026-09-10"

def test_categoria_numerica_lanza_error():
    with pytest.raises(CategoriaInvalidaError):
        Gasto(categoria="123", importe=10.0, fecha="2026-09-10")
def test_fecha_invalida_lanza_error():
    with pytest.raises(FechaInvalidaError):
        Gasto(categoria="comida", importe=12.0, fecha="206-09-10")

def test_importe_negativo_lanza_error():
    with pytest.raises(ImporteInvalidoError):
        Gasto(categoria="ocio", importe=-2.0, fecha="2026-08-11")

def test_falta_clave_lanza_datos_incompletos_error():
    datos_incompletos = {"categoria": "comida", "importe": 10.0}  # falta "fecha"
    with pytest.raises(DatosIncompletosError):
        dict_a_gasto(datos_incompletos)
