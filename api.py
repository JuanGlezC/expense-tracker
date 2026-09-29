from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from gestor import GestorGastos
from typing import Optional, List
from gasto import Gasto
from fastapi import Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from excepciones import CategoriaInvalidaError, ImporteInvalidoError, FechaInvalidaError, DatosIncompletosError
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



RUTA_DATOS = Path(os.getenv("RUTA_DATOS", "transacciones.json"))
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("Falta la variable de entorno SECRET_KEY")

# Usuarios simulados: solo para practicar.
USUARIOS = {"bosco": "clave-de-prueba"}


class GastoInput(BaseModel):
    categoria: str
    importe: float
    fecha: str
    model_config = {
        "json_schema_extra": {
            "example": {"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
        }
    }


class LoginInput(BaseModel):
    usuario: str
    password: str
    model_config = {
        "json_schema_extra": {
            "example": {"usuario": "juan", "password":"mi-clave-de-ejemplo"}
        }
    }

esquema_bearer = HTTPBearer()

def verificar_token(credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer)) -> str:
    """Verifica si el token es válido o ha caducado"""
    try:
        payload = leer_token(credenciales.credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o caducado")
    return payload["sub"]


def crear_token(usuario: str) -> str:
    """Crea un token codificado para el usuario"""
    payload = {
        "sub": usuario,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def leer_token(token: str) -> dict:
    """decodifica el token para comprobar su validez con la secret key"""
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


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
    return JSONResponse(status_code=400, content={"error": str(exc)})

def get_gestor() -> GestorGastos:
    """crea un gestor para uso de la API"""
    return GestorGastos(RUTA_DATOS)


@app.post("/login")
async def login(datos: LoginInput):
    """Comprueba usuario y password para autenticar si el usuario es admitido"""
    # Contraseña en claro, la voy a usar de práctica. Futuramente la sustituiré por hash.
    if USUARIOS.get(datos.usuario) != datos.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"access_token": crear_token(datos.usuario), "token_type": "bearer"}


@app.post("/gastos", status_code=201, dependencies=[Depends(verificar_token)])
async def crear_un_gasto(gasto_input: GastoInput, gestor: GestorGastos = Depends(get_gestor)):
    """Crea un nuevo gasto y lo persiste. Requiere autenticación."""
    gasto = Gasto(
        categoria=gasto_input.categoria,
        importe=gasto_input.importe,
        fecha=gasto_input.fecha,
    )
    gestor.agregar(gasto)
    gestor.guardar()
    return gasto


@app.get("/gastos", response_model=List[Gasto], dependencies=[Depends(verificar_token)])
async def listar_gastos(categoria: Optional[str] = None, gestor: GestorGastos = Depends(get_gestor)):
    """Lista de gastos por categoria opcionalmente, si la categoria es ausente devuelve la lista completa. Requiere autenticación"""
    if categoria:
        return gestor.filtrar_por_categoria(categoria)
    return gestor.gastos


@app.get("/gastos/total", status_code=200, dependencies=[Depends(verificar_token)])
async def obtener_total(gestor: GestorGastos = Depends(get_gestor)):
    """Obtiene los importes totales sumados y los importes por categoria sumados. Requiere autenticación"""
    return {
        "total_general": gestor.total_general(),
        "por_categoria": gestor.total_por_categoria(),
    }


@app.get("/")
async def leer_raiz():
    """Mensaje de bienvenida de la API"""
    return {"mensaje": "Bienvenido a expense-tracker API"}