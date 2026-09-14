from storage import guardar_transacciones, cargar_transacciones
from models import validar_transaccion, CategoriaInvalidaError, filtrar_por_categoria, FechaInvalidaError
from pathlib import Path
from datetime import datetime

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
    except FechaInvalidaError as error:
        print(f"Error de fecha: {error}")
    finally:
        print(f"Validación de '{transaccion.get('categoria')}' finalizada")




#transacciones_validadas.append({"categoria": "Ocio", "importe": 20.0})
guardar_transacciones(transacciones_validadas, ruta)


transacciones_verificadas:list[dict] = cargar_transacciones(ruta)
print(transacciones_verificadas)
categoria="Ocio"
transacciones_agrupadas:list[dict]=filtrar_por_categoria(transacciones_verificadas,categoria)



def mostrar_transacciones(transacciones_agrupadas):
    for elemento in transacciones_agrupadas:

        print(elemento)



mostrar_transacciones(transacciones_agrupadas)