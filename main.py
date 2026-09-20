from storage import guardar_transacciones,gasto_a_dict,cargar_gastos_validados
from gasto import Gasto,filtrar_por_categoria,agregar_gasto,total_general,total_por_categoria
from pathlib import Path

from excepciones import CategoriaInvalidaError,FechaInvalidaError,ImporteInvalidoError
import argparse

import sys


ruta: Path = Path("transacciones.json")

parser = argparse.ArgumentParser(description="Gestor de gastos personales")

subparsers = parser.add_subparsers(dest="comando", required=True)

parser_add = subparsers.add_parser("add", help="Añadir un nuevo gasto")
parser_add.add_argument("--categoria", required=True, help="Categoría del gasto")
parser_add.add_argument("--importe", required=True, type=float, help="Importe del gasto")
parser_add.add_argument("--fecha", required=True, help="Fecha en formato YYYY-MM-DD")

parser_list = subparsers.add_parser("list", help="Listar gastos")
parser_list.add_argument("--categoria", required=False, help="Filtrar por categoría (opcional)")


parser_total = subparsers.add_parser("total", help="Ver el total de gastos")

args = parser.parse_args()








if args.comando == "add":
    try:
        nuevo = Gasto(categoria=args.categoria, importe=args.importe, fecha=args.fecha)
    except (CategoriaInvalidaError, FechaInvalidaError, ImporteInvalidoError) as error:
        print(f"No se pudo añadir el gasto: {error}")
        sys.exit(1)
    else:
        gastos = cargar_gastos_validados(ruta)
        gastos = agregar_gasto(gastos, nuevo)
        guardar_transacciones([gasto_a_dict(g) for g in gastos], ruta)
        print(f"Gasto añadido: {nuevo}")

elif args.comando == "list":
    gastos = cargar_gastos_validados(ruta)
    if args.categoria:
        gastos = filtrar_por_categoria(gastos, args.categoria)
    if not gastos:
        print("No hay gastos que mostrar.")
    else:
        for gasto in gastos:
            print(gasto)
            
elif args.comando == "total":
    gastos = cargar_gastos_validados(ruta)
    if not gastos:
                print("No hay ningun gasto que mostrar")
    else:
        print(f"Total general: {total_general(gastos):.2f}")
        for categoria, total in total_por_categoria(gastos).items():
            print(f"  {categoria}: {total:.2f}")
    

