# Guión para la presentación del proyecto

## Contexto

- Un grupo de personas no se ponen de acuerdo sobre qué series / películas ver.
- Muchas veces se acaba cediendo a alguna opción con la que ninguno está en realidad conforme.
- Este proyecto busca encontrar una serie / película con la que sí se esté conforme.
- Se valoran más series / películas de las que se podrían valorar conversando.
- Se muestran cartas (como en tinder) y se desliza cada una hacia la izquierda o hacia la derecha.
- Al final se muestra un resumen con los votos que ha habido para cada serie / película.

## Elección del lenguaje: Python

### ¿Por qué lo escogí? 
No lo he usado demasiado y quería probar algo distinto a Javascript / Typescript.

### Cosas que me han gustado
- La sintaxis, preferencia personal, es agradable a la vista.
- Comunidad inmensa. Herramientas complementarias de calidad: Pytest, pylint, poetry, fastapi,...
- El tipado gradual ayuda mucho

### Cosas que no me han gustado
- Chapucillas del lenguaje:
    - Tener que pasar self a los métodos de la clase.
    - Ausencia de atributos privados como tal.
    - `__init__.py`
- Programación funcional en python:
```python
if len(list(filter(lambda u: u.id == user_id, self.__users))) != 1:
    raise UserNotFoundInSession
```
```javascript
if (users.filter(u => u.id == userId).length != 1)
    throw new UserNotFoundInSession()
```

Está bien si te preocupas por buscar linters, task runners, type hinting, async, ...

## Task runner y manejador de dependencias: Poetry

- Estaba algo familiarizado con pip y no me gusta nada.
- Poetry recuerda un poco a npm/yarn y me gusta.
- Crea los venv y funciona bastante bien.
- Todavía es joven y no hay mucho contenido, buildpacks de heroku, etc... Todavía usan pip.
- pyproject.toml para definir el proyecto.
- Mejor utilizar un task runner real en vez de Poetry.
    - Hace falta taskipy para ciertas cosas.
    - Quedan comandos largos y no permite dependencia entre tareas y otras cosas
- Para manejar dependencias ningún problema y muy buena documentación.

## Test runner: Pytest

- Fixtures muy simples e intuitivas y sin más añadidos que los necesarios.
- Dos opciones para organizar los tests:
    - Poner la carpeta de tests fuera de la raíz de código (en este caso al mismo nivel que app).
    - Poner la carpeta de tests dentro de la raíz de código (dentro de app). He acabado decantándome por esta segunda, ya que hay relación entre los test unitarios y los módulos, por ejemplo: test_session.py y session.py.

- Dentro de `tests` he separado por integración y unitarios.
- `@pytest.mark.asyncio` para testear funciones async.

## Complementos a los tests

- Coverage: Codecov para medir cobertura
- Mutmut: Para los tests de mutación

## Servidor: Uvicorn

- Para el servidor en Python podemos elegir WSGI o ASGI.
- ASGI utiliza la funcionalidad asíncrona de Python introducida en las versiones modernas de Python.
- Paradigma similar al de NodeJS y que está demostrado funciona muy bien en servicios con uso intensivo de entrada y salida.

- Dentro de los servidores ASGI tenemos:
    - Hypercorn
    - Daphne
    - Uvicorn
    
- Estoy utilizando Uvicorn porque utiliza como implementación del loop uvloop (que es una implementación más rápida escrita en C) algo que no tiene Daphne y es más estable que Hypercorn que está en beta. 
- Sin embargo, no me compromete a nada porque puedo cambiarlo por otro más adelante sin tener que tocar una línea de código (los tres implementan el estándar ASGI).


## Microframework: FastAPI

Considerando frameworks con interfaz ASGI:

Empecé con Starlette:
- Descarté Django/Channels por ser demasiado pesado y no un microframework realmente.
- Quart tiene poca comunidad.
- Sanic hubiera sido otra opción, pero Starlette tenía mejor soporte para websockets, aunque como explicaré más adelante al final no los he usado.

Sí quería y tenía recogido en una historia de usuario tener documentación automática de la api con Swagger y no conseguí implementarlo en Starlette.

Por lo que acabé usando FastAPI, que tiene Starlette como base y cuenta con esta documentación de serie.

Además FastAPI tiene alguna conveniencia más como su inyección de dependencias que me ha sido muy útil en tests de integración.

