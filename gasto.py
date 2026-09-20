
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass
from excepciones import CategoriaInvalidaError,FechaInvalidaError,DatosIncompletosError,ImporteInvalidoError

@dataclass
class Gasto:
    categoria:str
    importe: float
    fecha: str

    def __post_init__(self):
        """Valida categoria, importe y fecha; lanza una excepcion especifica segun el campo que falle."""
        if not isinstance(self.categoria, str):
            raise CategoriaInvalidaError(f"La categoría debe ser texto: {self.categoria}")
        #valida que la categoria sea un string
        if self.categoria.isdigit():
            
            raise CategoriaInvalidaError(f"La categoria no puede estar compuesta solo por numeros: {self.categoria}")
        #valida que categoria no sea una cadena numerica

        try:
            importe = float(self.importe)
            self.importe=importe
        except ValueError:
                raise ImporteInvalidoError(f"El importe no es un número válido: {self.importe}")
        #valida que el importe sea un numero valido
        
        if not isinstance(self.fecha,str):
            raise FechaInvalidaError(f"La fecha debe ser texto: {self.fecha}")
        #valida que la fecha sea una cadena de texto
        
        if self.importe < 0:
            raise ImporteInvalidoError(f"El importe no puede ser negativo: {self.importe}")
        #valida que el importe no sea negativo

        try:
            datetime.strptime(self.fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError(f"Formato de fecha inválido: {self.fecha}")
        #valida que la fecha coincida con el valor admitido en la clase datetime
      


def filtrar_por_categoria(gastos:list[Gasto],categoria: str)->list[Gasto]:
    """devuelve una lista_gastos agrupando las categorias coincidentes en el argumento"""

    lista_gastos: list[Gasto]=[elemento for elemento in gastos if elemento.categoria==categoria]

    return lista_gastos



def total_por_categoria(gastos: list[Gasto]) -> dict[str, float]:
    """devuelve el total de importe por categoria coincidente en el argumento"""
    totales: defaultdict = defaultdict(float)
    for gasto in gastos:
        totales[gasto.categoria] += gasto.importe
    return dict(totales)


def total_general(gastos: list[Gasto]) -> float:
    """devuelve una suma del importe de todas las transacciones de la lista"""
    return sum(gasto.importe for gasto in gastos)


def agregar_gasto(gastos: list[Gasto], nuevo_gasto: Gasto) -> list[Gasto]:
    """agrega un nuevo gasto introducido en el argumento"""
    gastos.append(nuevo_gasto)
    return gastos

