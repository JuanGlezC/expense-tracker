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

    

@pytest.mark.parametrize("categoria,importe,fecha,excepcion_esperada", [
    ("123", 10.0, "2026-09-10", CategoriaInvalidaError),
    ("comida", -5.0, "2026-09-10", ImporteInvalidoError),
    ("comida", 10.0, "fecha-mala", FechaInvalidaError),
    (1.0, 10.0,"2026-02-11", CategoriaInvalidaError),
    ("comida","once","2026,04-10", ImporteInvalidoError),
    ("comida", 6.0, 20260310, FechaInvalidaError)
])
def test_gasto_invalido_lanza_excepcion_correcta(categoria, importe, fecha, excepcion_esperada):
    with pytest.raises(excepcion_esperada):
        Gasto(categoria=categoria, importe=importe, fecha=fecha)