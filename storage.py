import json
from pathlib import Path
from dataclasses import asdict
from gasto import Gasto
from excepciones import DatosIncompletosError



def guardar_transacciones(lista_transacciones: list, ruta_archivo: Path)->None:
    with open(ruta_archivo, "w") as archivo:
        json.dump(lista_transacciones, archivo, indent=2)



def cargar_transacciones(ruta_archivo:Path)->list[dict]:
    if ruta_archivo.exists():
        with open(ruta_archivo, "r") as archivo:
         transacciones_cargadas:list[dict] = json.load(archivo)
    else:
       transacciones_cargadas=[]

    return transacciones_cargadas


def dict_a_gasto(datos:dict)->Gasto:


    try:
        gasto=Gasto(**datos)

    except TypeError:
        raise DatosIncompletosError(f"Las claves no son correctas en {datos}")

    return gasto

def gasto_a_dict(gasto:Gasto)->dict:

   
    diccionario:dict=asdict(gasto)
    return diccionario
