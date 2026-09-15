

from datetime import datetime
from dataclasses import dataclass
from excepciones import CategoriaInvalidaError,FechaInvalidaError,DatosIncompletosError,ImporteInvalidoError

@dataclass
class Gasto:
    categoria:str
    importe: float
    fecha: str

    def __post_init__(self):
        if not isinstance(self.categoria, str):
            raise CategoriaInvalidaError(f"La categoría debe ser texto: {self.categoria}")

        try:
            importe = float(self.importe)
            self.importe=importe
        except ValueError:
                raise ImporteInvalidoError(f"El importe no es un número válido: {self.importe}")
        
        if not isinstance(self.fecha,str):
            raise FechaInvalidaError(f"La fecha debe ser texto: {self.fecha}")
        
        if self.importe < 0:
            raise ImporteInvalidoError(f"El importe no puede ser negativo: {self.importe}")

        try:
            datetime.strptime(self.fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError(f"Formato de fecha inválido: {self.fecha}")