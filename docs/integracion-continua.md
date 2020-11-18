## Integración continua

### Github Actions

Lo estoy utilizando para:

- Lint del código: [La configuración de PyLint](.pylintrc) y [la configuración de la action](.github/workflows/qa.yml).
- Construcción de la imagen que utilizo para testear, como explico [aquí](docs/contenedor-tests.md) solo se reconstruye si es necesario.
- Tests aprovechando la imagen del paso anterior. Este paso es dependiente del anterior, si hace falta reconstruir la imagen, este "esperaría". La configuración es también [esta](.github/workflows/qa.yml).

### Travis

Es el servicio de integración continua adicional que estoy utilizando para correr los tests en varias versiones de Python.

- He configurado 3.7, 3.8 y 3.9. Las tres forman parte de las [active releases de python](https://www.python.org/downloads/). La 2.7 y 3.6 no están porque _features_ como _@dataclass_ (justifico su uso [aquí](docs/dataclass.md)) o _async/await_ no están disponibles.
- Además, usa una caché para no tener que recrear el entorno virtual de poetry:
  - He configurado poetry para que no cree el entorno virtual en un directorio arbitrario: `poetry config virtualenvs.in-project true`.
  - He cacheado el directorio `venv` que se crea en su lugar.

He encontrado estas prácticas [aquí](https://github.com/python-poetry/poetry/issues/366) y se puede consultar el fichero resultante [aquí](.travis.yml).

Ejecuto `poetry run task test` para correr los tests.

### CircleCI

Por último, utilizo CircleCI para hacer los tests de cobertura recogidos en la [historia de usuario correspondiente](https://github.com/AlexMenor/que-vemos/issues/45). Para la visualización utilizo CodeCov.

[Esta](.circleci/config.yml) es la configuración de CircleCI.

Ejecuto `poetry run task cov` para generar informe de cobertura.

