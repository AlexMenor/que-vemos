## Microframework

Tras avanzar lógica de negocio, necesitamos un microframework que exponga operaciones al exterior mediante una interfaz REST y adicionalmente websockets.

En python podemos elegir (desde hace poco) entre un framework que implemente el estándar WSGI o el ASGI. Este último aprovecha las co-rutinas introducidas
en versiones modernas de python y por tanto mejora la utilización de CPU en servidores web que suelen hacer uso extensivo de I/O.

Muy relacionada con la elección de microframework está la elección de servidor. 
Como servidores ASGI tenemos:
- Uvicorn
- Daphne
- Hypercorn

Estoy utilizando Uvicorn porque utiliza como implementación del loop uvloop (que es una implementación más rápida escrita en C) algo que no tiene Daphne
y es más estable que Hypercorn que está en beta.
Sin embargo, no me compromete a nada porque puedo cambiarlo por otro más adelante sin tener que tocar una línea de código (los tres implementan el estándar ASGI).

En cuanto a microframeworks he considerado:
- Django/Channels: Hace Django compatible con async. Django es más un framework completo que un microframework.
- Starlette: Soporte para websockets, anotado con tipos, sin dependencias y muy rápido.
- Sanic: Maduro y con una interfaz muy limpia. Parecido a flask y con el mismo tratamiento de parámetros y cuerpo que starlette.
- Quart: Es una reimplementación de Flask para ASGI.
- FastAPI: Toma Starlette como base y añade conveniencias como validación, generación automática de documentación OpenAPI, sistema de inyección de dependencias, manejado de excepciones, etc...

Empecé a usar Starlette y FastAPI: Quería un microframework simple (django no lo es), que no me abstrajera demasiado de las peticiones y con mantenimiento y comunidad mediana detrás (punto en contra de Quart).
Sanic también cumplía estos requisitos, pero starlette cuenta con [una interfaz](https://www.starlette.io/endpoints/#websocketendpoint) para usar websockets muy cómoda.

Al final me decidí por FastAPI, cuenta con todas las ventajas de Starlette y la conveniencia de tener la documentación OpenAPI automáticamente implementada (intenté conseguir lo mismo en Starlette sin éxito), que además era [una historia de usuario](https://github.com/AlexMenor/que-vemos/issues/65).
También es más cómodo que starlette en el tratamiento de parámetros y cuerpo (se explica más abajo) sin dejar de permitir tratar con 
[peticiones a bajo nivel si es necesario](https://fastapi.tiangolo.com/advanced/using-request-directly/).

Además, su sistema de inyección de dependencias me ha sido muy útil en los tests de integración para hacer por ejemplo:
```python
watchables_store = InMemoryWatchablesStore()

session_handler_mocked = SessionHandlerDependency(watchables_store, Mock())

# Cambio la dependencia
app.dependency_overrides[session_handler_dependency] = session_handler_mocked

# Se ejecuta el test
yield session

# Deshago el cambio
app.dependency_overrides = {}
```

### Cómo lo uso
Las rutas las voy a declarar en [el directorio routes](routes), allí exporto un objeto de la clase `APIRouter` que importaré en [app.py](app/app.py) donde 
se "pegan" todas las rutas.
El objeto `router`, aparte de declarar todas las rutas con decoradores, sirve para definir un prefijo que llevarán todas ese rutas (en el caso de session routes `/session`) 
y una descripción para la documentación automática.
![Documentación rutas](img/documentacion-rutas.png)

En el decorador de cada ruta también documento las distintas respuestas que puede haber desde cada ruta, para que se vean reflejadas en Swagger también.
```python
@router.post("/{session_id}/user",
          responses={404: {'description': 'Session not found'},
                     409: {'description': 'Session already has the maximum number of users'}},
          status_code=201, response_model=UserPayload)
```

Desde cada ruta, utilizo el manejador de sesiones que he venido desarrollando hasta ahora. Este manejador se inyecta:
```python
async def user_joins_session(session_id: str, session_handler: SessionHandler = Depends(session_handler_dependency)):
```
FastAPI se encarga de dos cosas ahí: 
- Que session_id tenga el valor que se pase en el parámetro de la ruta (lo hemos especificado en el decorador).
- En caso de necesitar extraer el cuerpo la petición (y validarlo) podemos declarar un modelo:
```python
class Vote (BaseModel):
    """ Represents that an user wants (or not) to see a watchable """

    watchable_index: int
    content: bool
```
Si alguno de los campos no esta presente o es de un tipo distinto al anotado, FastAPI devuelve un status code 422 con los detalles
de la validación.
- Inyectar session_handler.

Para esto último declaro antes:
```python
class SessionHandlerDependency:
    def __init__(self, watchables_store: WatchablesStore, session_store: SessionStore):
        self.session_handler = SessionHandler(watchables_store, session_store)

    def __call__(self):
        return self.session_handler


session_handler_dependency = SessionHandlerDependency(InMemoryWatchablesStore(), InMemorySessionStore())
```

De esta forma, puedo pasar como argumentos las implementaciones de WatchablesStore y SessionStore que quiera (en este caso las dos en memoria)
y se inyecta en las rutas en las que se declare como la anterior.

Como he dicho antes, para juntarlo todo está [app.py](app/app.py):
```python
app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(session_routes.router)
```

Para implementar cualquier middleware, basta con extender la clase `BaseHTTPMiddleware` que provee FastAPI pero que está implementada en Starlette.
En esta clase hay que definir el método `dispatch`:
```python
async def dispatch(self, request, call_next):
```
Donde request es la petición y call_next es una co-rutina que nos devuelve la respuesta que se va a devolver
si usamos `await`. Esto nos permite definir middleware que tiene efectos cuando entra la petición y cuando sale la respuesta.
