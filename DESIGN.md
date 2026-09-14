1. Proposito:

La aplicación funciona como un gestor de gastos, mediante uso de estructuras JSON permitiéndonos añadir nuevos gastos
y realizar buscas y agrupaciones por importe, fecha y categoría

2. Requisitos Funcionales:

-Añadir un gasto (categoría,importe,fecha)
-Realizar un listado de gastos
-Filtrado de gastos por categoría
-Filtrado de gastos por fecha
-Ver gasto total por categoría
-No tendría sentido en este proyecto hacer un filtrado de gastos por nombre porque pueden ser redundantes y no buscamos de momento un CRUD ni loggins de usuarios, es un proyecto de prueba

3. Modelo de datos:

Gasto:
  - categoria: str
  - importe: float
  - fecha: str (formato ISO: "2026-09-14")

  4. Estructura de carpetas y archivos


-main.py: orquestador de la lógica del proyecto y llamada a métodos
-storage.py: guardado y cargado de datos
-models.py: validacion y filtrado de transacciones, futuramente sera añadido el filtrado por fecha
-transacciones.json: archivo en el que se irán alojando los gastos en fromato JSON para su uso en la lógica del programa, actua como almacén de persistencia simple
-READMe.md: Estructura y datos del proyecto
-requirements.txt: requerimientos de uso de la aplicación y versiones
-.gitignore: Fuera de la estructura publica del proyecto queda un archivo de comandos que utilizo como referencia y el archivo.json que actua como almacén de persistencia ya que el uso de pruebas que hago no tiene sentido que se comparta

5. Interfaz de uso (CLI)

Por implementar, diseño pensado:

python main.py add --categoria Comida --importe 15.50 --fecha 2026-09-14
python main.py list
python main.py list --categoria Comida
python main.py total
python main.py filtra_fecha --fecha 2026-08-13 

6. Decisiones técnicas y por qué

He decidido utilizar un json para almacenar los gastos dado que para el uso de prueba del proyecto es más que suficiente y al no tener
loggins ni cruds no merece la pena estructurar una base de datos cofnigurada para el proyecto, más adelante podemos valorar su implementación.

7. Fuera de alcance 

Esta versión no va a modificar ni borrar datos

