# Expense Tracker

Gestor de gastos personales en Python con persistencia en JSON mediante uso de CLI argparse.

## Instalación

pip install -r requirements.txt

## Uso

Comandos disponibles:

python main.py add 
python main.py list
python main.py total

Uso de comandos:

python main.py add: required: --categoria --importe --fecha
--categoria:no puede estar compuesta únicamente por números
--importe:debe ser un float con caracteres numericos
--fecha:debe ser un string con una fecha en formato valido de la clase datatime
ejemplo de uso main.py: 
```
python main.py add --categoria comida --importe 10.5 --fecha 2026-11-06
```
resultado: añade un gasto correcto a la lista de gastos

python main.py list:
--categoria: no puede estar compuesta únicamente por números
ejemplo de uso: 
```
python main.py list --categoria ocio
```
resultado: devuelve una lista con los objetos gasto que coincidan con la categoria de busqueda

python main.py total:
ejemplo de uso: 
```
python main.py total
```
resultado: imprime el total general y el desglose por categoría como texto formateado

## Estructura del proyecto

- `gasto.py` — definicion de clase gasto y validacion de datos
- `storage.py` — carga y guardado de datos en JSON y transforma de objeto gasto a diccionario y viceversa para futuras cargas y guardados
- `main.py` — punto de entrada y manejo del programa mediante CLI argparse
- `excepciones.py` — cuerpo de excepciones propias