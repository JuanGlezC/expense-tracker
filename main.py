from storage import guardar_transacciones,cargar_transacciones,dict_a_gasto,gasto_a_dict
from gasto import Gasto,filtrar_por_fecha,filtrar_por_categoria
from pathlib import Path
from datetime import datetime
from excepciones import CategoriaInvalidaError,FechaInvalidaError,ImporteInvalidoError,DatosIncompletosError

ruta: Path = Path("transacciones.json")
transacciones_actuales:list[dict]= cargar_transacciones(ruta)  # sigue siendo list[dict], porque así viene del JSON
gastos_validados:list[Gasto] = []
for transaccion_dict in transacciones_actuales:
    try:
        gasto = dict_a_gasto(transaccion_dict)   # aquí se dispara la validación de __post_init__
        gastos_validados.append(gasto)
    except (CategoriaInvalidaError, FechaInvalidaError, ImporteInvalidoError, DatosIncompletosError) as error:
        print(f"Transacción inválida: {error}")


diccionario_validado=[]
for gasto in gastos_validados:
    diccionario_validado.append(gasto_a_dict(gasto))

guardar_transacciones(diccionario_validado, ruta)


transacciones_verificadas:list[dict] = cargar_transacciones(ruta)

gastos_verificados:list[Gasto]=[]
for transaccion in transacciones_verificadas:
    gastos_verificados.append(dict_a_gasto(transaccion))


gastos_filtrados:list[Gasto]=filtrar_por_categoria(gastos_verificados,"ocio")
print(gastos_filtrados)



def mostrar_transacciones(transacciones_agrupadas):
    for elemento in transacciones_agrupadas:

        print(elemento)
