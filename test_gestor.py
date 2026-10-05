from gasto import Gasto
from gestor import GestorGastos


def test_gestor_arranca_con_lista_vacia(engine_test):
    gestor = GestorGastos(engine_test)
    assert gestor.listar() == []


def test_agregar_persiste_el_gasto(engine_test):
    gestor = GestorGastos(engine_test)
    nuevo_gasto = Gasto(categoria="comida", importe=10.0, fecha="2026-09-10")

    gestor.agregar(nuevo_gasto)

    assert gestor.listar() == [nuevo_gasto]


def test_filtrar_por_categoria(engine_test):
    gestor = GestorGastos(engine_test)
    gestor.agregar(Gasto(categoria="comida", importe=10.0, fecha="2026-09-10"))
    gestor.agregar(Gasto(categoria="ocio", importe=20.0, fecha="2026-09-11"))

    resultado = gestor.filtrar_por_categoria("comida")

    assert len(resultado) == 1
    assert resultado[0].categoria == "comida"


def test_total_por_categoria(engine_test):
    gestor = GestorGastos(engine_test)
    gestor.agregar(Gasto(categoria="comida", importe=10.0, fecha="2026-09-10"))
    gestor.agregar(Gasto(categoria="comida", importe=5.0, fecha="2026-09-11"))
    gestor.agregar(Gasto(categoria="ocio", importe=20.0, fecha="2026-09-12"))

    assert gestor.total_por_categoria() == {"comida": 15.0, "ocio": 20.0}


def test_total_general(engine_test):
    gestor = GestorGastos(engine_test)
    gestor.agregar(Gasto(categoria="comida", importe=10.0, fecha="2026-09-10"))
    gestor.agregar(Gasto(categoria="ocio", importe=20.0, fecha="2026-09-11"))

    assert gestor.total_general() == 30.0


def test_id_se_mantiene_tras_recargar_con_otro_gestor(engine_test):
    nuevo_gasto = Gasto(categoria="comida", importe=10.0, fecha="2026-09-10")
    id_original = nuevo_gasto.id

    GestorGastos(engine_test).agregar(nuevo_gasto)

    gestor_nuevo = GestorGastos(engine_test)
    assert gestor_nuevo.listar()[0].id == id_original



    
