# ¿Qué vemos?

<p align="center">
  <img width="500" height="500" src="docs/img/logo.png">
</p>

> "Lemur designed by Freepik"

## El problema

¿Te agobia la indecisión al elegir una nueva serie que empezar? ¿No encuentras una película que haga justicia a las palomitas que acabas de hacer?

¿Y no es aún peor cuando esta decisión la tienes que tomar junto a tus padres? ¿O tu pareja?

## ¿Por qué he elegido este problema?

- Tengo personalmente este problema y me motiva resolverlo.
- De cara a la implementación me parece un proyecto interesante. Tiene fuentes de datos externas, persistencia temporal, REST y Websockets. Además, si tengo tiempo me gustaría diseñar un frontend que consuma el servicio.

## Interacción con el usuario

"Qué vemos" hace una selección de contenido, muestra una sucesión de películas/series en uno o varios clientes con conexión a internet (móvil, ordenador, ...) y cada uno decide si hacer "swipe left" o "swipe right". En cuanto haya una candidata en común, la selección parará y se mostrará la elección del grupo.

## Planteamiento del servicio

El servicio servirá peticiones de clientes a través de HTTP, con una API REST. Además hará uso de Websockets de forma puntual, entre otras cosas para hacer _push_ de alertas a los clientes (por ejemplo, que se ha encontrado una serie que les gusta a todos).
Necesita una fuente de datos (series y películas), que se concretará más adelante.

## Herramientas

- **Python**: Utilizando _features_ modernas del lenguaje, como _async/await_ o _typing_.
- **Framework Web**: Que permita especificar de forma declarativa endpoints (REST y Websockets) y los documente automáticamente conforme a algún estándar, por ejemplo Open API.
- **Logging**: Para conocer mejor el uso que los usuarios hacen del servicio e identificar problemas.
- **Fuente de datos de películas y series**: API externa, crawler o base de datos ya populada. En cualquier caso, tiene que estar "al día".
- **Memoria de sesiones**: Cuando los usuarios interactúan con el servicio, en alguna parte se tienen que almacenar temporalmente estructuras de datos que representen las elecciones que están haciendo.
- **Administrador de dependencias**: He elegido [poetry](https://python-poetry.org/), que hace una gestión de los entornos virtuales y de las dependencias muy cómoda.

## Documentación adicional

- [Configuración de git](docs/configurando-git.md)
- [Planteamiento de implementación](docs/pasos.md)
- [Historias de usuario y milestones](docs/hu-and-milestones.md)

## Comandos

### Instalación de dependencias

```bash
poetry install
```

> Require Poetry instalado en el sistema. Este comando creará un virtualenv en un subdirectorio de \$HOME (donde se ha instalado Poetry) e instalará las dependencias necesarias.

### Lint

El proyecto utiliza [pylint](https://www.pylint.org/) para hacer comprobaciones de sintaxis y estilo:

```bash
pylint app/
```
