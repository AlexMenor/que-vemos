# ¿Qué vemos?

<p align="center">
  <img width="500" height="500" src="docs/img/logo.png">
</p>

> "Lemur designed by Freepik"

## El problema

¿Te agobia la indecisión al elegir una nueva serie que empezar? ¿No encuentras una película que haga justicia a las palomitas que acabas de hacer? 

¿Y no es aún peor cuando esta decisión la tienes que tomar junto a tus padres? ¿O tu pareja? 

## Interacción con el usuario

"Qué vemos" hace una selección de contenido, muestra una sucesión de películas/series en uno o varios clientes con conexión a internet (móvil, ordenador, ...) y cada uno decide si hacer "swipe left" o "swipe right". En cuanto haya una candidata en común, la selección parará y se mostrará la elección del grupo.

## Planteamiento del servicio

El servicio servirá peticiones de clientes a través de HTTP, con una API REST. Además hará uso de Websockets de forma puntual, entre otras cosas para hacer *push* de alertas a los clientes (por ejemplo, que se ha encontrado una serie que les gusta a todos). 
Necesita una fuente de datos (series y películas), que se concretará más adelante.

## Herramientas
- **Python**: Utilizando *features* modernas del lenguaje, como *async/await* o *typing*.
- **Framework Web**: Que permita especificar de forma declarativa endpoints (REST y Websockets) y los documente automáticamente conforme a algún estándar, por ejemplo Open API.
- **Logging**: Para conocer mejor el uso que los usuarios hacen del servicio e identificar problemas.
- **Fuente de datos de películas y series**: API externa, crawler o base de datos ya populada. En cualquier caso, tiene que estar "al día".
- **Memoria de sesiones**: Cuando los usuarios interactúan con el servicio, en alguna parte se tienen que almacenar temporalmente estructuras de datos que representen las elecciones que están haciendo.

## Documentación adicional
- [Configuración de git](docs/configurando-git.md)
- [Planteamiento de implementación](docs/pasos.md)
