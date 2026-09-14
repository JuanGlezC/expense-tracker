class CategoriaInvalidaError(Exception):
    pass

def validar_transaccion(transaccion):

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



def agrupar_totales_por_categoria(lista_transacciones):

    totales={}
    for elemento in lista_transacciones:
        if elemento["categoria"] not in totales:
            totales[elemento["categoria"]]=elemento["importe"]

        else:
            totales[elemento["categoria"]]+= elemento["importe"]

    return totales





