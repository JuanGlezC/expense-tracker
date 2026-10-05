# expense-tracker

API REST para registrar gastos por categoría, con autenticación JWT, base de datos PostgreSQL, migraciones versionadas y tests de integración. Todo el sistema se levanta con Docker Compose.

## Tecnologías

Python 3.14 · FastAPI · Pydantic · SQLAlchemy 2 · PostgreSQL 18 · Alembic · pytest · Docker Compose · uv

## Puesta en marcha

Requisitos: Docker Desktop.

1. Crea tu archivo de configuración a partir del ejemplo y rellena los valores:

```powershell
Copy-Item .env.example .env
```

El archivo `.env` necesita dos variables: `DB_PASSWORD` (contraseña de PostgreSQL) y `SECRET_KEY` (clave para firmar los tokens JWT, larga y aleatoria).

2. Levanta la base de datos y la API:

```powershell
docker compose up -d --build
```

3. Crea las tablas ejecutando las migraciones (solo la primera vez en una base nueva):

```powershell
docker compose run --rm api alembic upgrade head
```

4. Abre la documentación interactiva en http://localhost:8000/docs.

Usuario de práctica para el login: `bosco` / `clave-de-prueba`. Es un usuario simulado, solo para desarrollo.

## Desarrollo local y tests

Requisitos: Python 3.14 y [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
docker compose up -d db
docker exec -it expense-tracker-db-1 psql -U postgres -c "CREATE DATABASE expense_tracker_test;"
python -m pytest -v
```

Los tests usan una base de datos separada (`expense_tracker_test`) que se vacía antes de cada test, así que nunca tocan tus datos reales. La base de test se crea una sola vez.

Para ejecutar la API fuera de Docker: `python -m uvicorn api:app --reload`.

## Estructura

| Archivo | Responsabilidad |
|---|---|
| `api.py` | Endpoints, validación de entrada, autenticación JWT, manejo de errores HTTP |
| `gestor.py` | Lógica de aplicación (`GestorGastos`) |
| `gasto.py` | Dominio: dataclass `Gasto`, reglas de validación y funciones puras de cálculo |
| `storage.py` | Único acceso a la base de datos |
| `GastoORM.py` | Modelo de la tabla `gastos` |
| `database.py` | Conexión (engine) a PostgreSQL |
| `alembic/` | Migraciones del esquema |
| `Dockerfile`, `docker-compose.yml` | Contenedores de la API y la base de datos |

## Documentación

- [API.md](API.md): endpoints, formato de peticiones y códigos de estado.
- [DESIGN.md](DESIGN.md): decisiones de diseño y su justificación.

## Limitaciones conocidas

- Los usuarios están definidos en el código con contraseña en claro (solo práctica); en un sistema real irían en base de datos con hash.
- Los filtros y totales se calculan en Python tras leer todas las filas; con muchos datos habría que hacerlos en SQL (`WHERE`, `SUM`, `GROUP BY`).
- La columna `descripcion` existe en la tabla pero el dominio aún no la usa.