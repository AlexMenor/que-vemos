## Diseño de la API

### Rutas e historias de usuario
- ` POST /session`: Crea una sesión y devuelve su id (que es un UUID v4). Devuelve siempre un `201 CREATED` y corresponde a 
[HU2: Como usuario debo ser capaz de crear un "grupo" para que los demás se puedan unir de forma fácil](https://github.com/AlexMenor/que-vemos/issues/14)
- `POST /session/{session_id}/user`: Crea un usuario dentro de una sesión y corresponde a [HU11: Como usuario quiero poder unirme a un grupo ya existente](https://github.com/AlexMenor/que-vemos/issues/66). Si la sesión no existe devuelve `404 NOT FOUND` y si la sesión tiene ya el número máximo de usuarios devuelve `409 CONFLICT`.
Si todo va bien, devuelve `201 CREATED` y en el cuerpo este schema:
```python
{
  "user_id": "string",
  "session_id": "string",
  "watchables": [
    {
      "title": "string",
      "synopsis": "string",
      "year": 0,
      "type": "MOVIE",
      "poster": "string",
      "popularity": 0
    }
  ]
}
```
El `user_id` es en este caso también un uuid v4 que se usará junto a `session_id` para emitir un voto.
- `POST /session/{session_id}/user/{user_id}/vote `: Emite un voto en una sesión de un usuario a un "Watchable" y corresponde a [HU3: Como usuario, debo poder decidir si me gustaría o no ver una película / serie](https://github.com/AlexMenor/que-vemos/issues/23).
Require un cuerpo con este schema:
```
{
  "watchable_index": 0,
  "content": true
}
```
Si la sesión o el usuario no existen se devuelve un `404 NOT FOUND`.
Si `watchable_index` no es un índice válido en el array de "Watchables" se devuelve `400 BAD REQUEST`.
Si los tipos del cuerpo son incorrectos o algún campo no está presente, se devuelve `422 VALIDATION ERROR`.
En caso contrario se devuelve `201 CREATED`.
- `GET /session/{session_id}/summary`: Devuelve un resumen de la sesión y corresponde a [HU12: Como usuario quiero ver los resultados al final de la votación](https://github.com/AlexMenor/que-vemos/issues/67).
Si la sesión no existe devuelve `404 NOT FOUND`, de lo contrario devuelve `200 OK`
y un body con [este esquema.](app/entities/session_summary.py)

### Diseño por capas

En la aplicación se pueden ver tres capas diferenciadas:
- Interfaz: Expone rutas HTTP y trata las peticiones que llegan.
La forman: Servidor (Uvicorn), microframework (FastAPI), [middleware](app/middleware), [rutas](app/routes) y [app.py](app/app.py).
Para testear el código escrito en estos dos últimos (además de la integración de las capas) están [los tests de integración](app/tests/integration/test_session_routes.py).
- Lógica: [Entidades](app/entities) y [session_handler](app/session_handler.py).
- Persistencia: Todo bajo el directorio [data](app/data).
Se definen las interfaces de persistencia ([SessionStore](app/data/session_store/session_store.py) y [WatchablesStore](app/data/watchables_store/watchables_store.py)) y sus implementaciones (de momento solo persisten en memoria).
Además, contiene el script que extrae los datos todos los días [WatchablesExtractor](app/data/watchables_extractor/watchables_extractor.py).

Se ha aplicado inversión del control de forma que la interfaz y la persistencia dependan de la lógica y nunca al revés.
