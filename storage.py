import json
from pathlib import Path
from dataclasses import asdict
from gasto import Gasto
from excepciones import DatosIncompletosError,CategoriaInvalidaError,ImporteInvalidoError,FechaInvalidaError
import json


def guardar_transacciones(lista_transacciones: list, ruta_archivo: Path)->None:
    with open(ruta_archivo, "w") as archivo:
        json.dump(lista_transacciones, archivo, indent=2)





def cargar_transacciones(ruta_archivo: Path) -> list[dict]:
    if not ruta_archivo.exists():
        return []
    with open(ruta_archivo, "r") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError as error:
            print(f"Error: el archivo {ruta_archivo} está corrupto o no es JSON válido: {error}")
            return []


def dict_a_gasto(datos:dict)->Gasto:


    try:
        gasto=Gasto(**datos)

    except TypeError:
        raise DatosIncompletosError(f"Las claves no son correctas en {datos}")

    return gasto

def gasto_a_dict(gasto:Gasto)->dict:

   
    diccionario:dict=asdict(gasto)
    return diccionario

def cargar_gastos_validados(ruta_archivo: Path) -> list[Gasto]:
    transacciones_dict = cargar_transacciones(ruta_archivo)
    gastos = []
    for transaccion in transacciones_dict:
        try:
            gastos.append(dict_a_gasto(transaccion))
        except (CategoriaInvalidaError, FechaInvalidaError, ImporteInvalidoError, DatosIncompletosError) as error:
            print(f"Transacción inválida ignorada: {error}")
    return gastos
