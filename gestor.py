from gasto import Gasto, filtrar_por_categoria as filtrar_gastos_por_categoria, total_general as calcular_total_general, total_por_categoria as calcular_total_por_categoria
from storage import agregar_gasto, cargar_gastos
from decoradores import log_llamada
import logging
logging.basicConfig(level=logging.INFO)

class GestorGastos:
    def __init__(self, engine):
        self.engine = engine

    @log_llamada
    def agregar(self, nuevo_gasto: Gasto) -> None:
        """persiste el gasto inmediatamente en la base de datos"""
        agregar_gasto(self.engine, nuevo_gasto)

    def filtrar_por_categoria(self, categoria: str) -> list[Gasto]:
        """consulta todos los gastos actuales y filtra por categoría"""
        gastos = cargar_gastos(self.engine)
        return filtrar_gastos_por_categoria(gastos, categoria)

    def total_general(self) -> float:
        gastos = cargar_gastos(self.engine)
        return calcular_total_general(gastos)

    def total_por_categoria(self) -> dict[str, float]:
        gastos = cargar_gastos(self.engine)
        return calcular_total_por_categoria(gastos)
    
    def listar(self) -> list[Gasto]:
        """devuelve todos los gastos actuales de la base de datos"""
        return cargar_gastos(self.engine)