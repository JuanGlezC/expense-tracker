from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class GastoInput(BaseModel):

    categoria: str
    importe: float
    fecha: str


@app.post("/gastos")
def crear_un_gasto(gasto: GastoInput):
    return {"recibido": gasto}





@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a expense-tracker API"}