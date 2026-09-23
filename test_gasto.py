from gasto import Gasto
from excepciones import CategoriaInvalidaError,FechaInvalidaError,ImporteInvalidoError,DatosIncompletosError
import pytest


@pytest.fixture
def gasto_valido():
    return Gasto(categoria="comida", importe=15.5, fecha="2026-09-10")


def test_gasto_valido_se_crea_correctamente(gasto_valido):
    
    assert gasto_valido.categoria == "comida"
    assert gasto_valido.importe == 15.5
    assert gasto_valido.fecha == "2026-09-10"

def test_categoria_numerica_lanza_error():
    with pytest.raises(CategoriaInvalidaError):
        Gasto(categoria="123", importe=10.0, fecha="2026-09-10")
def test_fecha_invalida_lanza_error():
    with pytest.raises(FechaInvalidaError):
        Gasto(categoria="comida", importe=12.0, fecha="206-09-10")

def test_importe_negativo_lanza_error():
    with pytest.raises(ImporteInvalidoError):
        Gasto(categoria="ocio", importe=-2.0, fecha="2026-08-11")
