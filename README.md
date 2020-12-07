# ¿Qué vemos?
![que-vemos gha](https://github.com/AlexMenor/que-vemos/workflows/que-vemos%20QA/badge.svg)
![que-vemos travis](https://travis-ci.com/AlexMenor/que-vemos.svg?branch=master)
[![codecov](https://codecov.io/gh/AlexMenor/que-vemos/branch/master/graph/badge.svg?token=DGPWNVEISN)](https://codecov.io/gh/AlexMenor/que-vemos)
[![Netlify Status](https://api.netlify.com/api/v1/badges/9256fdf3-62b9-44c4-8238-cccaa06b7c23/deploy-status)](https://app.netlify.com/sites/amazing-villani-e2d732/deploys)

<p align="center">
  <img width="500" height="500" src="docs/img/logo.png">
</p>

> Lemur designed by Freepik

¿Te agobia la indecisión al elegir una nueva serie que empezar? ¿No encuentras una película que haga justicia a las palomitas que acabas de hacer?

¿Y no es aún peor cuando esta decisión la tienes que tomar junto a tus padres? ¿O tu pareja?

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
- Quart: Es una reimplementación de Flask para ASGI.
- FastAPI: Toma Starlette como base y añade conveniencias como validación, generación automática de documentación OpenAPI, sistema de inyección de dependencias, manejado de excepciones, etc...

Empecé a usar Starlette y FastAPI: Quería un microframework simple (django no lo es), que no me abstrajera demasiado de las peticiones y con mantenimiento y comunidad mediana detrás (punto en contra de Quart).

Al final me decidí por FastAPI por la conveniencia de tener la documentación OpenAPI automáticamente implementada (intenté conseguir lo mismo en Starlette sin éxito).

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
El objeto `router`, aparte de declarar todas las rutas con decoradores, defino un prefijo que llevarán todas ese rutas (en el caso de session routes `/session`) 
y una descripción para la documentación automática.
![Documentación rutas](docs/img/documentacion-rutas.png)

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




## Comandos

### Instalación de dependencias

```bash
poetry install
```

> Requiere Poetry instalado en el sistema. Este comando creará un virtualenv en un subdirectorio de \$HOME (donde se ha instalado Poetry) e instalará las dependencias necesarias.

### Lint

El proyecto utiliza [pylint](https://www.pylint.org/) para hacer **comprobaciones de sintaxis y estilo**:

```bash
poetry run task lint
```

### Test

Utilizo [pytest](https://docs.pytest.org/en/stable/):

```bash
poetry run task test
```

### Informe de cobertura

```bash
poetry run task cov
```

### Tests de mutación

```bash
poetry run task mut
```

## Documentación adicional

- [Configuración de git](docs/configurando-git.md)
- [Pasos de implementación](docs/pasos.md)
- [Más detalles del problema](docs/problema.md)
- [Historias de usuario y milestones](docs/hu-and-milestones.md)
- [Primer avance de código](app/entities/watchable.py)
- [Justificación de uso de @dataclass](docs/dataclass.md)
- [Sobre el task runner, Poetry](docs/task-runner.md)
- [¿Cómo se testea el proyecto?](docs/tests.md)
- [Contenedor entorno de tests](docs/contenedor-tests.md)
- [Integración continua](docs/integracion-continua.md)
- [Serverless](docs/serverless.md)
- [Tests de mutación](docs/tests-mutacion.md)


## Agradecimientos
![movie db](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg)

Por el acceso a [su API.](https://www.themoviedb.org/documentation/api)
