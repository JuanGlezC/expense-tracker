from gestor import GestorGastos
from gasto import Gasto
import pytest

def test_gestor_arranca_con_lista_vacia_si_archivo_no_existe(tmp_path):
    ruta = tmp_path / "gastos_test.json"
    gestor = GestorGastos(ruta)
    assert gestor.gastos == []


def test_agregar_y_guardar_persiste_el_gasto(tmp_path):
    ruta = tmp_path / "gastos_test.json"
    gestor = GestorGastos(ruta)
    nuevo_gasto = Gasto(categoria="comida", importe=10.0, fecha="2026-09-10")
    gestor.agregar(nuevo_gasto)
    gestor.guardar()

    gestor_verificacion = GestorGastos(ruta)
    assert len(gestor_verificacion.gastos) == 1
    assert gestor_verificacion.gastos[0].categoria == "comida"




def test_filtrar_por_categoria(tmp_path):
    ruta = tmp_path / "gastos_test.json"
    gestor = GestorGastos(ruta)
    
    gestor.agregar(Gasto(categoria="comida", importe=10.0, fecha="2026-09-10"))
    gestor.agregar(Gasto(categoria="comida", importe=7.5, fecha="2026-08-11"))
    gestor.agregar(Gasto(categoria="ocio", importe=12.0, fecha="2026-05-12"))

    resultado = gestor.filtrar_por_categoria("comida")
    assert len(resultado) == 2  
    assert all(gasto.categoria == "comida" for gasto in resultado)




    
