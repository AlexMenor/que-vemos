## ¿Por qué he elegido este problema?

- Tengo personalmente este problema y me motiva resolverlo.
- De cara a la implementación me parece un proyecto interesante. Tiene fuentes de datos externas, persistencia temporal, REST y Websockets. Además, si tengo tiempo me gustaría diseñar un frontend que consuma el servicio.

## Interacción con el usuario

"Qué vemos" hace una selección de contenido, muestra una sucesión de películas/series en uno o varios clientes con conexión a internet (móvil, ordenador, ...) y cada uno decide si hacer "swipe left" o "swipe right". En cuanto haya una candidata en común, la selección parará y se mostrará la elección del grupo.

## Planteamiento del servicio

El servicio servirá peticiones de clientes a través de HTTP, con una API REST. Además hará uso de Websockets de forma puntual, entre otras cosas para hacer _push_ de alertas a los clientes (por ejemplo, que se ha encontrado una serie que les gusta a todos).
Necesita una fuente de datos (series y películas), que se concretará más adelante.
