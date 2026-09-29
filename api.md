# Expense Tracker API

## Arrancar el servidor

uv sync
uv run uvicorn api:app --reload

Documentación interactiva en http://127.0.0.1:8000/docs

## Autenticación

POST /login con usuario y contraseña devuelve un token JWT.
Los endpoints de /gastos requieren el header:
Authorization: Bearer <token>

Ejemplo de login:

{"usuario": "Juan", "password": "mi-clave-secreto"}

Respuesta esperada:
{"access_token": "eyJhbGci...", "token_type": "bearer"}

## Endpoints

### POST /gastos

- Body: {"categoria": str, "importe": float, "fecha": str}
- Éxito: 201 Created — devuelve el gasto creado, incluyendo el id generado por el servidor
- Error: 400/422 si categoria, importe o fecha no pasan la validación de Gasto
- Ejemplo de respuesta (201):
{
  "id": "3d4be023-f325-43c7-8f40-0946e06af87f",
  "categoria": "comida",
  "importe": 10.5,
  "fecha": "2026-09-10"
}


### GET /gastos

- Query param opcional: ?categoria=comida
- Éxito: 200 OK — devuelve una lista de gastos (todos, o filtrados por categoría)
- Ejemplo de respuesta (200), sin filtro:
[
  {"id": "3d4be023-...", "categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"},
  {"id": "4587ae54-...", "categoria": "ocio", "importe": 20.0, "fecha": "2026-09-14"}
]
- Ejemplo de respuesta (200), con ?categoria=comida:
[
  {"id": "3d4be023-...", "categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
]

### GET /gastos/total

- Sin parámetros
- Éxito: 200 OK — devuelve el total general y el desglose por categoría
- Ejemplo de respuesta (200):
{
  "total_general": 66.0,
  "por_categoria": {"comida": 51.5, "ocio": 14.5}
}