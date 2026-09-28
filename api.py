from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from gestor import GestorGastos
from typing import Optional,List
from gasto import Gasto
from fastapi import Request, Depends, Header,HTTPException
from fastapi.responses import JSONResponse
from excepciones import CategoriaInvalidaError,ImporteInvalidoError,FechaInvalidaError,DatosIncompletosError
from dotenv import load_dotenv
import os




app = FastAPI()

load_dotenv()
RUTA_DATOS = Path(os.getenv("RUTA_DATOS", "transacciones.json"))
API_KEY = os.getenv("API_KEY")




class GastoInput(BaseModel):

    categoria: str
    importe: float
    fecha: str

def verificar_api_key(x_api_key: str = Header(default=None)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key es ausente")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="La API Key es inválida")



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

@app.post("/gastos", status_code=201, dependencies=[Depends(verificar_api_key)])
async def crear_un_gasto(gasto_input: GastoInput, gestor: GestorGastos = Depends(get_gestor)):
    gasto = Gasto(
        categoria=gasto_input.categoria,
        importe=gasto_input.importe,
        fecha=gasto_input.fecha
    )
    
    gestor.agregar(gasto)
    gestor.guardar()
    return gasto



@app.get("/gastos", response_model=List[Gasto], dependencies=[Depends(verificar_api_key)])
async def listar_gastos(categoria: Optional[str] = None, gestor: GestorGastos = Depends(get_gestor)):
    
    if categoria:
        return gestor.filtrar_por_categoria(categoria)
    return gestor.gastos

@app.get("/gastos/total", status_code=200, dependencies=[Depends(verificar_api_key)])
async def obtener_total(gestor: GestorGastos = Depends(get_gestor)):
    
    return{
        "total_general": gestor.total_general(),
        "por_categoria": gestor.total_por_categoria()
    }

@app.get("/")
async def leer_raiz():
    return {"mensaje": "Bienvenido a expense-tracker API"}