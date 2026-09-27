from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from gestor import GestorGastos
from typing import Optional,List
from gasto import Gasto
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from excepciones import CategoriaInvalidaError,ImporteInvalidoError,FechaInvalidaError,DatosIncompletosError

app = FastAPI()

RUTA_DATOS = Path("transacciones.json")


class GastoInput(BaseModel):

    categoria: str
    importe: float
    fecha: str



@app.exception_handler(CategoriaInvalidaError)
def manejar_categoria_invalida(request: Request, exc: CategoriaInvalidaError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@app.exception_handler(ImporteInvalidoError)
def manejar_importe_invalido(request: Request, exc: ImporteInvalidoError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@app.exception_handler(FechaInvalidaError)
def manejar_fecha_invalida(request: Request, exc: FechaInvalidaError):
    return JSONResponse(status_code=400, content={"error": str(exc)})
@app.exception_handler(DatosIncompletosError)
def manejar_datos_incompletos(request: Request, exc: DatosIncompletosError):
    return JSONResponse(status_code=400, content={"error":str(exc)})


def get_gestor() -> GestorGastos:
    return GestorGastos(RUTA_DATOS)

@app.post("/gastos", status_code=201)
async def crear_un_gasto(gasto_input: GastoInput, gestor: GestorGastos = Depends(get_gestor)):
    gasto = Gasto(
        categoria=gasto_input.categoria,
        importe=gasto_input.importe,
        fecha=gasto_input.fecha
    )
    
    gestor.agregar(gasto)
    gestor.guardar()
    return gasto



@app.get("/gastos", response_model=List[Gasto])
async def listar_gastos(categoria: Optional[str] = None, gestor: GestorGastos = Depends(get_gestor)):
    
    if categoria:
        return gestor.filtrar_por_categoria(categoria)
    return gestor.gastos

@app.get("/gastos/total", status_code=200)
async def obtener_total(gestor: GestorGastos = Depends(get_gestor)):
    
    return{
        "total_general": gestor.total_general(),
        "por_categoria": gestor.total_por_categoria()
    }

@app.get("/")
async def leer_raiz():
    return {"mensaje": "Bienvenido a expense-tracker API"}