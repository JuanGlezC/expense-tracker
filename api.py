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


@app.post("/gastos", status_code=201)
def crear_un_gasto(gasto_input: GastoInput):
    gasto = Gasto(
        categoria=gasto_input.categoria,
        importe=gasto_input.importe,
        fecha=gasto_input.fecha
    )
    gestor = GestorGastos(RUTA_DATOS)
    gestor.agregar(gasto)
    gestor.guardar()
    return gasto



@app.get("/gastos", response_model=List[Gasto])
def listar_gastos(categoria: Optional[str] = None):
    gestor = GestorGastos(RUTA_DATOS)
    if categoria:
        return gestor.filtrar_por_categoria(categoria)
    return gestor.gastos

@app.get("/gastos/total", status_code=201)
def obtener_total():
    gestor=GestorGastos(RUTA_DATOS)
    return{
        "total_general": gestor.total_general(),
        "por_categoria": gestor.total_por_categoria()
    }

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a expense-tracker API"}