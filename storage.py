import json
from pathlib import Path



def guardar_transacciones(lista_transacciones: list, ruta_archivo: Path)->None:
    with open(ruta_archivo, "w") as archivo:
        json.dump(lista_transacciones, archivo, indent=2)



def cargar_transacciones(ruta_archivo:Path)->list[dict]:
    if ruta_archivo.exists():
        with open(ruta_archivo, "r") as archivo:
         datos_cargados:list[dict] = json.load(archivo)
    else:
       datos_cargados=[]

    return datos_cargados