## Tests

Utilizo [pytest](https://docs.pytest.org/en/stable/) porque la forma de hacer fixtures es muy simple y no hay apenas añadidos a python puro, es muy intuitiva.

En la documentación de _pytest_ se recogen dos patrones comunes: Poner la carpeta de tests fuera de la raíz de código (en este caso al mismo nivel que app) y poner la carpeta de tests dentro de la raíz de código (dentro de app). He acabado decantándome por esta segunda, ya que hay relación entre los test unitarios y los módulos, por ejemplo: `test_session.py` y `session.py.`

El primer patrón tiene sentido cuando los test son más funcionales.

[Mi primer fichero de tests.](app/tests/test_session.py)

He añadido también una _github action_ que los ejecuta:

![GH Action Tests](docs/img/tests.png)

## Primera clase testeable

[Session](app/entities/session.py) representa el grupo de personas indecisas sobre qué película o serie ver. Para testearla basta con hacer `poetry run task test` (previo `poetry install`).
