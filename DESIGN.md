1. Proposito:

La aplicación funciona como un gestor de gastos, mediante uso de estructuras JSON permitiéndonos añadir nuevos gastos
y realizar buscas y agrupaciones por importe, fecha y categoría, agregar nuevos gastos y carga y guardado en el archivo de forma automatica

2. Requisitos Funcionales:

-Añadir un gasto (categoría,importe,fecha)
-Realizar un listado de gastos
-Filtrado de gastos por categoría
-Ver gasto total por categoría
-No tendría sentido en este proyecto hacer un filtrado de gastos por nombre porque pueden ser redundantes y no buscamos de momento un CRUD ni loggins de usuarios, es un proyecto de prueba

3. Modelo de datos:

Gasto:
  - categoria: str
  - importe: float
  - fecha: str (formato ISO: "2026-09-14")
  - Id: str

GestorGastos

  - ruta: path
  - self.gastos: list[Gasto]

  4. Estructura de carpetas y archivos


-gasto.py— definicion de clase gasto y validacion de datos
-storage.py— carga y guardado de datos en JSON y transforma de objeto gasto a diccionario y viceversa para futuras cargas y guardados
-main.py— punto de entrada y manejo del programa mediante CLI argparse
-gestor.py— definicion de gestorGastos y uso de metodos de gasto de forma simplificada
-excepciones.py— cuerpo de excepciones propias
-test_*.py— cuerpo de test y debug
-decoradores.py— estructura y cuerpo de envolturas para las funciones
-transacciones.json: archivo en el que se irán alojando los gastos en fromato JSON para su uso en la lógica del programa, actua como almacén de persistencia simple
-READMe.md: Estructura y datos del proyecto
-pyproject.toml: requerimientos de uso de la aplicación y versiones
-uv.lock: instalacion que se realizara con el programa
-.gitignore: Fuera de la estructura publica del proyecto queda un archivo de comandos que utilizo como referencia y el archivo.json que actua como almacén de persistencia ya que el uso de pruebas que hago no tiene sentido que se comparta hace uso de .venv/

5. Interfaz de uso (CLI)


python main.py add --categoria Comida --importe 15.50 --fecha 2026-09-14
python main.py list
python main.py list --categoria Comida
python main.py total

Las salidas ahora incluyen linea de log


6. Decisiones técnicas y por qué

- He decidido utilizar un json para almacenar los gastos dado que para el uso de prueba del proyecto es más que suficiente y al no tener
loggins ni cruds no merece la pena estructurar una base de datos cofnigurada para el proyecto, más adelante podemos valorar su implementación.

- El proyecto usa gestión de dependencias con uv, tests con pytest (cobertura ~80%+), y logging estructurado
- El diseño del proyecto sigue principios SOLID, especialmente responsabilidad única (cada módulo tiene una única razón de cambio) y abierto/cerrado (nuevas funciones de filtrado se añaden sin modificar código existente)

7. Fuera de alcance 

Esta versión no va a modificar ni borrar datos

8. Validacion

"El sistema es sensible a mayúsculas/minúsculas en la categoría ('Comida' y 'comida' se tratan como categorías distintas). Normalizar esto (por ejemplo, forzando minúsculas en __post_init__) queda pendiente como mejora futura."

--categoria: str que no sean cadenas unicamente numericas
--importe: float valido
--fecha: string que se ajusten al formato de clase datatime

9. Métodos API


- Add -> Petición POST: Body: JSON ejemplo POST/gastos {"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
- List -> Petición GET: ejemplo GET/gastos?categoria=comida /categoria es opcional
- Total -> Petición GET: ejemplo: GET/gastos/total

Respuestas esperadas: 
- 201 para creación exitosa 
- 200 para lecturas exitosas 
- 400/422 para datos inválidos
- 404 no existe el recurso
- 500 error del servidor