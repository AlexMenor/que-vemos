# ¿Qué vemos?

<p align="center">
  <img width="500" height="500" src="docs/img/logo.png">
</p>

> "Lemur designed by Freepik"

## El problema

¿Te agobia la indecisión al elegir una nueva serie que empezar? ¿No encuentras una película que haga justicia a las palomitas que acabas de hacer?

¿Y no es aún peor cuando esta decisión la tienes que tomar junto a tus padres? ¿O tu pareja?

## Herramientas

- **Python**: Utilizando _features_ modernas del lenguaje, como _async/await_ o _typing_.
- **Framework Web**: Que permita especificar de forma declarativa endpoints (_REST_ y _Websockets_) y los documente automáticamente conforme a algún estándar, por ejemplo _Open API_.
- **Logging**: Para conocer mejor el uso que los usuarios hacen del servicio e identificar problemas.
- **Fuente de datos de películas y series**: API externa, crawler o base de datos ya populada. En cualquier caso, tiene que estar "al día".
- **Memoria de sesiones**: Cuando los usuarios interactúan con el servicio, en alguna parte se tienen que almacenar temporalmente estructuras de datos que representen las elecciones que están haciendo.

## Integración continua

### Github Actions

![que-vemos gha](https://github.com/AlexMenor/que-vemos/workflows/que-vemos%20QA/badge.svg)

Lo estoy utilizando para:

- Lint del código: [La configuración de PyLint](.pylintrc) y [la configuración de la action](.github/workflows/qa.yml).
- Construcción de la imagen que utilizo para testear, como explico [aquí](docs/contenedor-tests) solo se reconstruye si es necesario.
- Tests aprovechando la imagen del paso anterior. Este paso es dependiente del anterior, si hace falta reconstruir la imagen, este "esperaría". La configuración es también [esta](.github/workflows/qa.yml).

### Travis

![que-vemos travis](https://travis-ci.com/AlexMenor/que-vemos.svg?branch=master)

Es el servicio de integración continua adicional que estoy utilizando para correr los tests en varias versiones de Python.

- He configurado 3.7, 3.8 y 3.9. La 3.6 no está porque _@dataclass_ no está disponible. Justifico su uso [aquí](docs/dataclass.md).
- Además, usa una caché para no tener que recrear el entorno virtual de poetry:
  - He configurado poetry para que no cree el entorno virtual en un directorio arbitrario: `poetry config virtualenvs.in-project true`.
  - He cacheado el directorio `venv` que se crea en su lugar.

En definitiva, he seguido las prácticas que he encontrado [aquí](https://github.com/python-poetry/poetry/issues/366) y se puede consultar el fichero resultante [aquí](.travis.yml).

Ejecuto `poetry run task test` para correr los tests.

### CircleCI

[![codecov](https://codecov.io/gh/AlexMenor/que-vemos/branch/master/graph/badge.svg?token=DGPWNVEISN)](https://codecov.io/gh/AlexMenor/que-vemos)

Por último, utilizo CircleCI para hacer los tests de cobertura recogidos en la [historia de usuario correspondiente](https://github.com/AlexMenor/que-vemos/issues/45). Para la visualización utilizo CodeCov.

[Esta](.circleci/config.yml) es la configuración de CircleCI.

Ejecuto `poetry run task cov` para generar informe de cobertura.

## Avance de código

Para este hito he avanzado el código para [la historia de usuario 2](https://github.com/AlexMenor/que-vemos/issues/14):

- [SessionHandler](app/session_handler.py) se encargará de administrar todas las sesiones de la aplicación.
- [UserPayload](app/entities/user_payload.py) representa la información que necesita un usuario para votar a lo largo de la sesión.
- [Estos](app/tests/test_session_handler.py) son los tests para la lógica de SessionHandler.

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
