# ¿Qué vemos?
![que-vemos CI/CD](https://github.com/AlexMenor/que-vemos/workflows/que-vemos%20CI/CD/badge.svg)
![que-vemos travis](https://travis-ci.com/AlexMenor/que-vemos.svg?branch=master)
[![codecov](https://codecov.io/gh/AlexMenor/que-vemos/branch/master/graph/badge.svg?token=DGPWNVEISN)](https://codecov.io/gh/AlexMenor/que-vemos)
[![Netlify Status](https://api.netlify.com/api/v1/badges/9256fdf3-62b9-44c4-8238-cccaa06b7c23/deploy-status)](https://app.netlify.com/sites/amazing-villani-e2d732/deploys)

<p align="center">
  <img width="500" height="500" src="docs/img/logo.png">
</p>

> Lemur designed by Freepik

¿Te agobia la indecisión al elegir una nueva serie que empezar? ¿No encuentras una película que haga justicia a las palomitas que acabas de hacer?

¿Y no es aún peor cuando esta decisión la tienes que tomar junto a tus padres? ¿O tu pareja?

<p align="center">
  <img width="360" height="640" src="docs/img/que-vemos-preview.gif">
</p>

- [Despliegue en PaaS](docs/paas.md)
- [Implementación de persistencia (redis) y uso dentro del PaaS](docs/bd.md)
- [Pruebas de prestaciones](docs/prestaciones.md)
- [Diseño de la API (no es nuevo)](docs/diseño-api.md)
- **Se puede probar la aplicación con el frontend [aquí](https://amazing-villani-e2d732.netlify.app/)**

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

### Iniciar microservicio

```bash
poetry run task start
```

### Iniciar microservicio para desarrollo

En este modo al hacer cambios en cualquier fichero, la aplicación se reinicia.

```bash
poetry run task dev
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
- [Elección de microframework](docs/microframework.md)
- [Configuración del microservicio](docs/configuracion.md)
- [Configuración de logs](docs/logs.md)
- [Tests de integración](docs/tests-integracion.md)

## Agradecimientos

![movie db](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg)

Por el acceso a [su API.](https://www.themoviedb.org/documentation/api)
