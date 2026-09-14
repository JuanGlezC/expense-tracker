from storage import guardar_transacciones, cargar_transacciones
from models import validar_transaccion, agrupar_totales_por_categoria, CategoriaInvalidaError
from pathlib import Path


ruta: Path = Path("transacciones.json")
transacciones_actuales:list[dict] = cargar_transacciones(ruta)
# añade una transacción nueva con .append(...)

transacciones_validadas:list=[]
for transaccion in transacciones_actuales:
    try:
        validar_transaccion(transaccion)
        print(f"{transaccion['categoria']}: válido")
        transacciones_validadas.append(transaccion)
    except KeyError as error:
        print(f"Error de datos incompletos: {error}")
    except ValueError as error:
        print(f"Error de formato: {error}")
    except CategoriaInvalidaError as error:
        print(f"Error de negocio: {error}")
    finally:
        print(f"Validación de '{transaccion.get('categoria')}' finalizada")




transacciones_validadas.append({"categoria": "Ocio", "importe": 20.0})
guardar_transacciones(transacciones_validadas, ruta)


transacciones_verificadas:list[dict] = cargar_transacciones(ruta)
print(transacciones_verificadas)

transacciones_agrupadas:dict=agrupar_totales_por_categoria(transacciones_verificadas)



def mostrar_totales(transacciones_agrupadas):
    for clave,valor in transacciones_agrupadas.items():

        print(f"El valor total de la categoria {clave} es {valor:.2f}")



mostrar_totales(transacciones_agrupadas)