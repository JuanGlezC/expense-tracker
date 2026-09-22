from gestor import GestorGastos
from gasto import Gasto
from pathlib import Path
from excepciones import CategoriaInvalidaError, FechaInvalidaError, ImporteInvalidoError
import argparse
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
        logger.error(f"No se pudo añadir el gasto: {error}")
        sys.exit(1)
    else:
        gestor = GestorGastos(ruta)
        gestor.agregar(nuevo)
        gestor.guardar()
        logger.info(f"Gasto añadido correctamente: {nuevo}")
elif args.comando == "list":
        gestor = GestorGastos(ruta)
        gastos = gestor.filtrar_por_categoria(args.categoria) if args.categoria else gestor.gastos
        if not gastos:
            print("No hay gastos que mostrar.")
        else:
            for gasto in gastos:
                print(gasto)
        
            
elif args.comando == "total":
    gestor = GestorGastos(ruta)
    if not gestor.gastos:
        print("No hay ningun gasto que mostrar")
    else:
        print(f"Total general: {gestor.total_general():.2f}")
        for categoria, total in gestor.total_por_categoria().items():
            print(f"  {categoria}: {total:.2f}")

