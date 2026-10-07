# API de expense-tracker

Base: `http://localhost:8000`. Documentación interactiva: `/docs`.

## Autenticación

Todos los endpoints de `/gastos` requieren un token JWT en la cabecera:

```
Authorization: Bearer <access_token>
```

El token se obtiene en `POST /login` y caduca a los 30 minutos.

## Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/` | No | Mensaje de bienvenida |
| POST | `/login` | No | Devuelve un token de acceso |
| POST | `/gastos` | Sí | Crea un gasto |
| GET | `/gastos` | Sí | Lista gastos; filtro opcional `?categoria=comida` |
| GET | `/gastos/total` | Sí | Total general y total por categoría |

### POST /login

Petición:

```json
{"usuario": "bosco", "password": "clave-de-prueba"}
```

Respuesta 200:

```json
{"access_token": "eyJ...", "token_type": "bearer"}
```

### POST /gastos

Petición:

```json
{"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10"}
```

Respuesta 201 (el `id` lo genera el servidor):

```json
{"categoria": "comida", "importe": 10.5, "fecha": "2026-09-10", "id": "3a390560-5ce1-4959-ac13-7d227c098468"}
```

### GET /gastos

Respuesta 200: lista de gastos con el mismo formato que arriba. Con `?categoria=comida` devuelve solo los de esa categoría.

### GET /gastos/total

Respuesta 200:

```json
{"total_general": 15.0, "por_categoria": {"comida": 10.0, "ocio": 5.0}}
```

## Códigos de error

| Código | Cuándo |
|---|---|
| 400 | El dato tiene el tipo correcto pero rompe una regla de negocio (categoría numérica, importe negativo, fecha con formato incorrecto). Cuerpo: `{"error": "mensaje"}` |
| 401 | Falta el token, es inválido o ha caducado, o el login es incorrecto |
| 422 | El cuerpo no encaja con el esquema (campo ausente o tipo incorrecto, por ejemplo `"importe": "abc"`) |

Reglas de negocio de un gasto: la categoría no puede ser solo números, el importe debe ser mayor o igual que 0 y la fecha debe tener formato `AAAA-MM-DD`.