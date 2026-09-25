from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from gestor import GestorGastos
from typing import Optional,List
from gasto import Gasto

app = FastAPI()

RUTA_DATOS = Path("transacciones.json")

class GastoInput(BaseModel):

    categoria: str
    importe: float
    fecha: str






@app.get("/gastos", response_model=List[Gasto])
def listar_gastos(categoria: Optional[str] = None):
    gestor = GestorGastos(RUTA_DATOS)
    if categoria:
        return gestor.filtrar_por_categoria(categoria)
    return gestor.gastos



@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a expense-tracker API"}