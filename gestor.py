from gasto import Gasto, filtrar_por_categoria as filtrar_gastos_por_categoria, total_general as calcular_total_general, total_por_categoria as calcular_total_por_categoria
from storage import cargar_gastos_validados,guardar_transacciones,gasto_a_dict
from pathlib import Path
from decoradores import log_llamada


class GestorGastos:
    def __init__(self, ruta: Path):
        """constructor con ruta"""
        self.ruta = ruta
        self.gastos: list[Gasto] = cargar_gastos_validados(ruta)
        
    @log_llamada
    def agregar(self, nuevo_gasto: Gasto) -> None:
        """agrega un nuevo gasto a la lista de gastos"""
        self.gastos.append(nuevo_gasto)

    def filtrar_por_categoria(self, categoria: str) -> list[Gasto]:
        """agrupa todos los gastos de una caregoria"""
        return filtrar_gastos_por_categoria(self.gastos, categoria)  # reutiliza la función suelta

    def total_general(self) -> float:
        """calcula el total general de importes"""
        return calcular_total_general(self.gastos)  # idem

    def total_por_categoria(self) -> dict[str, float]:
        """devuelve el total de importe por categoria coincidente en el argumento"""
        return calcular_total_por_categoria(self.gastos)  # idem

    def guardar(self) -> None:
        """guarda en el json la lista de transacciones indicadas en la ruta del argumento"""
        guardar_transacciones([gasto_a_dict(g) for g in self.gastos], self.ruta)