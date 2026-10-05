import pytest
from sqlalchemy.exc import IntegrityError

from gasto import Gasto
from storage import agregar_gasto, cargar_gastos


def test_cargar_gastos_con_tabla_vacia(engine_test):
    assert cargar_gastos(engine_test) == []


def test_agregar_y_cargar_gasto(engine_test):
    gasto = Gasto(categoria="comida", importe=10.5, fecha="2026-09-10")
    agregar_gasto(engine_test, gasto)

    assert cargar_gastos(engine_test) == [gasto]


def test_id_duplicado_viola_la_clave_primaria(engine_test):
    gasto = Gasto(categoria="comida", importe=1.0, fecha="2026-09-10")
    agregar_gasto(engine_test, gasto)

    with pytest.raises(IntegrityError):
        agregar_gasto(engine_test, gasto)