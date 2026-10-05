import pytest
from sqlalchemy.exc import IntegrityError

from gasto import Gasto
from storage import agregar_gasto, cargar_gastos, agregar_gastos


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

def test_agregar_gastos_es_todo_o_nada(engine_test):
    existente = Gasto(categoria="comida", importe=1.0, fecha="2026-09-10")
    agregar_gasto(engine_test, existente)

    valido = Gasto(categoria="ocio", importe=5.0, fecha="2026-09-11")

    with pytest.raises(IntegrityError):
        agregar_gastos(engine_test, [valido, existente])

    assert cargar_gastos(engine_test) == [existente]


def test_sin_transaccion_unica_se_guarda_a_medias(engine_test):
    existente = Gasto(categoria="comida", importe=1.0, fecha="2026-09-10")
    agregar_gasto(engine_test, existente)

    valido = Gasto(categoria="ocio", importe=5.0, fecha="2026-09-11")

    with pytest.raises(IntegrityError):
        for gasto in [valido, existente]:
            agregar_gasto(engine_test, gasto)

    assert len(cargar_gastos(engine_test)) == 2