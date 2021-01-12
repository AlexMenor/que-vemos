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
- Todavía es joven y mucho contenido, buildpacks de heroku, etc... Todavía usan pip.
- pyproject.toml para definir el proyecto.
- Mejor utilizar un task runner real en vez de Poetry.
    - Hace falta taskipy para ciertas cosas.
    - Quedan comandos largos y no permite dependencia entre tareas y otras cosas
- Para manejar dependencias ningún problema y muy buena documentación.
