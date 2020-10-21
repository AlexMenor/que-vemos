## Administración de dependencias y tareas: Poetry

De manera análoga a `package.json` en Node, Poetry utiliza `pyproject.toml` para definir todas las dependencias de nuestro paquete.

Por defecto, crea un entorno virtual en nuestro sistema con todas las dependencias y la versión de python especificadas en `pyproject.toml.`

Además permite ejecutar comandos dentro de este entorno con `poetry run`, por lo que podemos hacer `poetry run pytest` por ejemplo.

Sin embargo, he preferido añadir una dependencia de desarrollo que se llama [taskipy](https://pypi.org/project/taskipy/) que permite añadir en `pyproject.toml` alias de comandos más largos, por ejemplo: `poetry run pylint app` se queda en `poetry run task lint` (en este caso es igual de largo, pero más genérico).
