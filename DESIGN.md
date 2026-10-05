DESIGN — expense-tracker

Documento de diseño del proyecto: qué hace, cómo está montado y por qué tomé cada decisión. Se actualiza cuando cambia el diseño, no solo el código.

1. Propósito

La aplicación es un gestor de gastos. Permite añadir nuevos gastos, listarlos, filtrarlos por categoría y ver el total general y por categoría.

Empezó como un programa de consola que guardaba los gastos en un archivo JSON. Después pasó a ser una API REST con autenticación y, en la última fase, los datos se guardan en una base de datos PostgreSQL y todo el sistema se levanta con Docker Compose.

2. Requisitos funcionales
Añadir un gasto (categoría, importe, fecha).
Listar los gastos.
Filtrar los gastos por categoría.
Ver el gasto total, general y por categoría.

No tendría sentido en este proyecto filtrar los gastos por nombre, porque pueden ser redundantes. De momento tampoco busco un CRUD completo ni un sistema real de usuarios: es un proyecto de práctica.

3. Fuera de alcance

Esta versión no modifica ni borra gastos.

4. Modelo de datos

El mismo gasto existe en tres formas distintas, cada una con su responsabilidad (ver sección 10.3).

Gasto (dominio, dataclass en gasto.py):

categoria: str
importe: float
fecha: str (formato ISO: "2026-09-14")
id: str (UUID generado automáticamente si no se indica)

GastoORM (tabla gastos en PostgreSQL, GastoORM.py):

id: str, clave primaria
categoria: str
importe: float
fecha: str
descripcion: str, opcional. Existe en la tabla desde la segunda migración, pero el dominio todavía no la usa; queda reservada para una ampliación futura.

GastoInput (entrada de la API, Pydantic en api.py):

categoria: str, importe: float, fecha: str. No incluye id, que lo genera el servidor.

GestorGastos (gestor.py):

engine: la conexión a la base de datos. Ya no guarda una lista de gastos en memoria: cada consulta lee de la base.
5. Validación

Las reglas de negocio están en __post_init__ del dataclass Gasto:

categoria: texto que no sea únicamente numérico.
importe: un número válido y mayor o igual que 0.
fecha: una cadena que se ajuste al formato AAAA-MM-DD (el de la clase datetime).

La validación se reparte en dos niveles. Pydantic comprueba los tipos (¿es un texto? ¿es un número?) y responde 422 si no encajan. El dominio comprueba las reglas (¿tiene sentido?) y lanza excepciones propias que la API convierte en 400.

Pendiente: el sistema distingue mayúsculas y minúsculas en la categoría ("Comida" y "comida" se tratan como categorías distintas). Normalizar esto, por ejemplo forzando minúsculas en __post_init__, queda como mejora futura.

6. Estructura de carpetas y archivos

Código de la aplicación

api.py: la API REST (endpoints, validación de entrada, autenticación y manejo de errores HTTP).
gestor.py: definición de GestorGastos y uso de los métodos del dominio de forma simplificada.
gasto.py: dataclass Gasto, sus reglas de validación y las funciones puras de filtrado y totales.
storage.py: única puerta de acceso a la base de datos (agregar_gasto, agregar_gastos, cargar_gastos).
GastoORM.py: modelo SQLAlchemy de la tabla gastos.
database.py: creación del engine (conexión) a PostgreSQL.
excepciones.py: excepciones propias.
decoradores.py: envolturas para las funciones (registro de llamadas).
main.py: punto de entrada de la versión de consola con argparse (ver sección 7).

Base de datos y despliegue

alembic/: configuración y migraciones del esquema.
Dockerfile, .dockerignore, docker-compose.yml: contenedores de la API y de la base de datos.

Tests

conftest.py: fixtures compartidas (base de test y limpieza).
test_*.py: tests de API, gestor, storage y dominio.

Configuración y documentación

.env: secretos y configuración local (DB_PASSWORD, SECRET_KEY). .env.example es la plantilla pública.
README.md: cómo ponerlo en marcha. API.md: referencia de la API. DESIGN.md: este documento.
pyproject.toml: requisitos de la aplicación y versiones.
uv.lock: versiones exactas que se instalan.
.gitignore: deja fuera de la parte pública el entorno .venv/, el .env y mis archivos de comandos y pruebas de referencia, que no aportan nada a quien lea el proyecto.
7. Interfaz de uso

La interfaz principal es la API REST (sección 8). Se usa desde http://localhost:8000/docs o con cualquier cliente HTTP.

La versión original de consola funcionaba así:

python main.py add --categoria Comida --importe 15.50 --fecha 2026-09-14
python main.py list
python main.py list --categoria Comida
python main.py total

Las salidas incluyen una línea de log. Esta interfaz pertenece a la versión con JSON; queda pendiente decidir si se mantiene adaptada a PostgreSQL o se elimina.

8. API REST

Alcance: la API solo opera sobre la colección completa de gastos (crear y consultar). No expone rutas /gastos/{id} para editar o borrar un gasto individual, aunque el modelo Gasto ya incluye un campo id (UUID) generado automáticamente, pensado para soportar esas operaciones en una versión futura.

Endpoints síncronos y asíncronos: los endpoints que consultan la base de datos están definidos con def normal, no con async def. SQLAlchemy es síncrono, y una llamada bloqueante dentro de un async def bloquearía el bucle de eventos de toda la aplicación; con def, FastAPI ejecuta cada petición en un hilo aparte. POST /login y GET / siguen siendo async porque no acceden a la base de datos. (En la versión con JSON los dejé todos async como anticipación del diseño; al llegar la base de datos lo corregí.)

CORS: el middleware está configurado de forma permisiva (todos los orígenes, métodos y cabeceras) para desarrollo local. Antes de un despliegue real habría que restringir allow_origins a los dominios reales del frontend.

POST /gastos
Body: {"categoria": str, "importe": float, "fecha": str}
Éxito: 201 Created, devuelve el gasto creado incluyendo el id generado por el servidor.
Error: 400 si categoría, importe o fecha no pasan las reglas de Gasto; 422 si el cuerpo no encaja con el esquema.
Ejemplo de respuesta (201):
json
{
  "id": "3d4be023-f325-43c7-8f40-0946e06af87f",
  "categoria": "comida",
  "importe": 10.5,
  "fecha": "2026-09-10"
}
GET /gastos
Query param opcional: ?categoria=comida
Éxito: 200 OK, devuelve una lista de gastos (todos, o filtrados por categoría).
Ejemplo de respuesta (200), sin filtro:
json
[
  {"id": "3d4be023-...", "categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"},
  {"id": "4587ae54-...", "categoria": "ocio", "importe": 20.0, "fecha": "2026-09-14"}
]
Ejemplo de respuesta (200), con ?categoria=comida:
json
[
  {"id": "3d4be023-...", "categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
]
GET /gastos/total
Sin parámetros.
Éxito: 200 OK, devuelve el total general y el desglose por categoría.
Ejemplo de respuesta (200):
json
{
  "total_general": 66.0,
  "por_categoria": {"comida": 51.5, "ocio": 14.5}
}
Errores comunes
400: el dato tiene el tipo correcto pero rompe una regla de negocio. Cuerpo: {"error": "mensaje"}.
401: falta el token, es inválido o ha caducado.
404: no aplica en la forma actual, porque no hay rutas con {id}.
422: el cuerpo no encaja con el esquema (campo ausente o tipo incorrecto).
500: fallo no controlado del servidor (por ejemplo, la base de datos no está disponible). Pendiente: devolver un error controlado en estos casos.
9. Autenticación
POST /login recibe usuario y contraseña simulados (sin base de datos, una tabla fija en memoria) y devuelve un JWT firmado con HS256 que caduca a los 30 minutos.
Los tres endpoints de /gastos requieren la cabecera Authorization: Bearer <token>.
.env: SECRET_KEY firma los tokens y nunca sale del servidor. Sustituye a la antigua API KEY por razones de seguridad. Si falta, la aplicación no arranca.
Pendiente: cambiar la validación de contraseña a hash antes de cualquier uso real.
10. Decisiones técnicas y por qué
10.1 Herramientas y principios
Gestión de dependencias con uv, tests con pytest (cobertura ~80%+) y logging estructurado.
El diseño sigue principios SOLID, especialmente responsabilidad única (cada módulo tiene una única razón de cambio) y abierto/cerrado (las nuevas funciones de filtrado se añaden sin modificar código existente).
10.2 Dónde se guardan los datos: de JSON a PostgreSQL

Decisión inicial: al empezar usé un archivo JSON para almacenar los gastos, porque para una prueba era más que suficiente y, sin logins ni CRUD, no merecía la pena configurar una base de datos.

Revisión: al convertir el proyecto en una API real, la persistencia pasó a PostgreSQL con SQLAlchemy. La persistencia deja de ser transacciones.json: ahora storage.py habla con PostgreSQL.

Motivo: el patrón del JSON era cargar todo, acumular en memoria y reescribir todo al guardar. Eso permite que una escritura sobrescriba y pierda los cambios de otra que ocurrió casi a la vez (una pérdida de actualización, o lost update). Con una base de datos cada inserción es independiente.

Consecuencias:

Eliminé guardar() de storage.py y la lista en memoria de GestorGastos: cada lectura va a la base de datos, así que los datos siempre están al día.
transacciones.json deja de usarse y se retira del repositorio.
10.3 Tres representaciones de un gasto

Decisión: Gasto (dominio), GastoORM (tabla) y GastoInput (entrada de la API) se mantienen como estructuras independientes.

Alternativa descartada: consideré fusionar el dataclass Gasto con GastoORM. Pensé que traería más problemas de arquitectura que ventajas: en caso de cambiar de base de datos, y a la hora de probar las reglas de negocio por separado, es mejor tener cada responsabilidad en su sitio.

Cómo queda cada una:

GastoInput comprueba los tipos de lo que llega por HTTP.
Gasto comprueba las reglas de negocio y no depende ni de HTTP ni de SQL.
GastoORM describe cómo se guarda en la base.

La respuesta de la API usa directamente el dataclass Gasto como response_model, sin una clase de salida aparte. storage.py es el único que traduce entre Gasto y GastoORM; el gestor nunca importa GastoORM.

10.4 La categoría es un texto, no una tabla

Decisión: la categoría es un campo de texto validado. No he creado una tabla de categorías al trabajar con la base de datos.

Motivo: los requisitos funcionales (sección 2) se cumplen perfectamente con la estructura actual. El usuario puede crear categorías con cualquier texto no numérico, así que no existe una necesidad real de una tabla categorias.

Revisión: se revisará si se añaden requisitos nuevos.

11. Esquema de la base de datos con Alembic

Decisión: las tablas dejan de crearse a mano (el CREATE TABLE manual). El esquema se versiona con Alembic: cada cambio en la estructura de la base de datos es una migración en alembic/versions/, con su upgrade() y su downgrade().

Motivo: si se cambia GastoORM sin tocar la base de datos, el código y la tabla quedan desincronizados y cualquier operación sobre gastos falla con "column does not exist". Con migraciones versionadas, cualquier base de datos (la de un compañero, un servidor de test, producción) llega al esquema actual ejecutando alembic upgrade head.

Regla: todo cambio en un modelo SQLAlchemy va acompañado de su migración (alembic revision --autogenerate), revisada a mano antes de aplicarla, y se commitea junto con el cambio del modelo.

Migraciones actuales:

412a92341086: crea la tabla gastos.
eb76f04759c3: añade la columna opcional descripcion (versión actual, head).

Tabla inicial: la tabla gastos creada a mano se borró y se regeneró con la primera migración, para que el historial de Alembic sea el único origen del esquema. Los datos que había eran solo de prueba.

Revisión futura: si apareciera una base de datos con datos reales anteriores a Alembic, se usaría alembic stamp en lugar de recrear la tabla.

12. Transacciones

Decisión: cada operación de storage.py abre su propia Session de SQLAlchemy, que equivale a una transacción. Las operaciones de varios pasos usan una única transacción para que sean atómicas (todo o nada).

Caso concreto: agregar_gastos guarda una lista de gastos con un solo commit. Si una fila falla (por ejemplo, un id duplicado), se hace rollback y no se guarda ninguna, ni siquiera las válidas que iban antes. La excepción se vuelve a lanzar para que quien llama sepa que falló.

Motivo: guardar los gastos uno a uno con agregar_gasto deja la base a medias si falla uno intermedio; hay un test que lo demuestra. Hoy cada endpoint guarda un solo gasto, pero una importación masiva futura necesitaría esta garantía.

13. Tests

Decisión: los tests de la API, del gestor y del storage se ejecutan contra una base de datos PostgreSQL real y separada (expense_tracker_test), no contra JSON temporal ni simulaciones.

Motivo: un test que no toca la base real no comprueba lo que falla en producción: tipos de columna, restricciones (NOT NULL, clave primaria) y el comportamiento del commit. Por ejemplo, guardar dos gastos con el mismo id no daba error con JSON, pero con PostgreSQL lanza IntegrityError, y hay un test que lo comprueba.

Cómo funciona:

conftest.py crea un engine para la base de test una vez por ejecución y crea la tabla con Base.metadata.create_all.
Una fixture autouse vacía la tabla (TRUNCATE) antes de cada test y sustituye get_gestor mediante dependency_overrides, de modo que ningún test puede escribir en mi base de desarrollo. Al terminar, restaura los overrides aunque el test falle.
Un gasto inválido no solo debe dar error: los tests también comprueban que no se guardó nada.

Alternativa descartada: abrir una transacción por test y hacer rollback al final. Es más rápida, pero oculta bugs relacionados con el commit, que es justo lo que quiero verificar.

Consecuencias:

Los tests necesitan el contenedor de la base arrancado.
La fixture autouse también se ejecuta en los tests unitarios de dominio, que no la necesitan; lo acepté por simplicidad.
La tabla de test se crea con create_all y no con Alembic, así que las migraciones no se prueban en este flujo.
14. Contenedores con Docker Compose

Decisión: la API y la base de datos se ejecutan como dos servicios de Docker Compose.

Imagen de la API: parte de python:3.14-slim e instala las dependencias con uv sync --frozen --no-dev en una capa anterior a la copia del código, para aprovechar la caché de capas: cambiar una línea de código no reinstala las dependencias. Esto exigió declarar uvicorn como dependencia de producción y no de desarrollo.
Red: dentro de Compose, la API encuentra la base por el nombre del servicio (db), no por localhost. Por eso el host se lee de la variable DB_HOST, con localhost por defecto para el desarrollo local.
Orden de arranque: la base define un healthcheck (pg_isready) y la API espera a que esté sana (depends_on con service_healthy).
Secretos: .env está en .dockerignore y no entra en la imagen; las variables se pasan al contenedor desde Compose.
Migraciones: se ejecutan a mano (docker compose run --rm api alembic upgrade head) y no al arrancar la API. Así se evita que varias instancias migren a la vez y se mantiene el control del momento en que cambia el esquema. El coste es un paso manual extra en una instalación nueva.
15. Limitaciones conocidas y mejoras futuras
Los usuarios están definidos en el código con la contraseña en claro (solo práctica). En un sistema real irían en base de datos con hash.
Los filtros y totales se calculan en Python tras leer todas las filas. Con muchos datos habría que hacerlos en SQL (WHERE, SUM, GROUP BY).
cargar_gastos vuelve a validar cada fila al reconstruir el Gasto: una fila corrupta en la base rompería todo el listado.
La columna descripcion existe en la tabla pero el dominio no la usa.
La categoría distingue mayúsculas y minúsculas.
Un fallo de la base de datos devuelve un 500 sin controlar.
Falta decidir si la versión de consola (main.py) se mantiene o se elimina.