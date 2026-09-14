
from datetime import datetime

class CategoriaInvalidaError(Exception):
    pass

class FechaInvalidaError(Exception):
     pass

def validar_transaccion(transaccion):

    if "fecha" not in transaccion:
        raise FechaInvalidaError(f"La clave fecha no existe en la transaccion: {transaccion}")
    try:
            texto_fecha=str(transaccion["fecha"])
            datetime.strptime(texto_fecha, "%Y-%m-%d")
    except ValueError:
        raise FechaInvalidaError(f"La fecha no tiene un formato valido en: {transaccion}")
                 
    
    if "importe" not in transaccion:
        raise KeyError(f"Falta la clave 'importe' en la transaccion: {transaccion}")

    try:
        importe = float(transaccion["importe"])
        transaccion["importe"]=importe
    except ValueError:
        raise ValueError(f"El importe no es un número válido: {transaccion['importe']}")
    

    if not isinstance(transaccion.get("categoria"), str):
        raise CategoriaInvalidaError(f"Categoria invalida en: {transaccion}")

    return True




def filtrar_por_categoria(lista_transacciones:list[dict],categoria: str)->list[dict]:

    lista_categoria: list[dict]=[elemento for elemento in lista_transacciones if elemento["categoria"]==categoria]

    return lista_categoria

def filtrar_por_fecha(lista_transacciones:list[dict], fecha: str)->list[dict]:

    lista_fechas: list[dict]=[elemento for elemento in lista_transacciones if elemento["fecha"]==fecha]

    return lista_fechas




