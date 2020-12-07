## Serverless
### Integración en el proyecto
Las funciones que he implementado para despliegue FaaS no son un prototipo del microservicio sino que responden a historias de usuario y serán útiles en el proyecto. Por eso, he creado [una carpeta](app/serverless) en `app` junto al resto del código para estas funciones y sus tests.
Más adelante explico el despliegue de esta parte.
### Get Trending Watchables
La primera función que he implementado usando serverless corresponde a [HU8: Como usuario, quiero poder obtener una lista de películas y series para ver ejemplos de lo que puedo elegir en la aplicación. Filtrar por películas/series, ordenarlas, buscar, ...](https://github.com/AlexMenor/que-vemos/issues/53).

Esta función la [he alojado en netlify](https://amazing-villani-e2d732.netlify.app/.netlify/functions/get_trending_watchables
) admite peticiones GET con los siguientes query parameters opcionales:
- 'type': Permite filtrar por tipo (películas o series) 'MOVIE' o 'SERIES'.
- 'search': Busca en las synopsis y títulos la cadena de caracteres proporcionada.
- 'orderBy': Ordena en base al siguiente criterio. `[campo],[orden]`. En `campo` admite 'popularity' y 'year'. En `orden` admite 'DESC' y 'ASC'.

[Esta](app/serverless/get_trending_watchables.js) es la función y [estos](app/serverless/test/trending_watchables.test.js) sus tests que se ejecutan automáticamente en [esta](.github/workflows/qa.yml) github action.

Además, he implementado [este frontend](https://amazing-villani-e2d732.netlify.app/) que se puede ver en [su carpeta](frontend) del repositorio.

![frontend](docs/img/frontend.png)

Mi intención es que esta función se llame cada vez que un usuario entre a la página, de esta forma lo primero que ve son unas cuantas películas y series entre las que decidir. Incentivando que inicie una sesión con alguien. 
Así, el microservicio que se implementará más adelante tiene menos carga y se dedica solamente a administrar las sesiones.

### Watchables Extractor
No directamente relacionado con serverless pero esencial para que la función anterior funcione y obtener todas estas películas y series he implementado un script en Python que es ejecutado por una Github Action diariamente.
- Obtiene los datos de [the movie db](https://www.themoviedb.org/). En concreto, las películas y series "trending" del día.
- Los parsea para instanciar entidades de mi aplicación.
- Serializa las instancias con pickle en binario, pensado para que el microservicio los consuma, y en JSON para que las funciones serverless (que he escrito en JS) los utilicen.
- Por último hace commit y push al repositorio.

El script [es este](app/data/watchables_extractor/watchables_extractor.py), los test son [estos](app/tests/unit/test_watchables_extractor.py) y la github action es [esta](.github/workflows/refresh-data.yml).

### Send Feedback
La otra función que he implementado usando FaaS corresponde a [HU9: Como desarrollador, quiero que los usuarios puedan dar feedback fácilmente.](https://github.com/AlexMenor/que-vemos/issues/58)
- Solo admite el método POST y devuelve un código 405 (method not allowed) de lo contrario.
- Solo admite un cuerpo con formato: `{"feedback":[string]}`, de lo contrario devuelve un código 400 (bad request).
- Hace un _profanity filter_ en inglés con el mensaje y devuelve 400 si es ofensivo.
- Por último, usando la API de Telegram, envía el mensaje a través de un bot a [este canal](https://t.me/sugerenciasQueVemos).

Esta función se usa también en el frontend.

![feedback](docs/img/feedback.png)

La función es [esta](app/serverless/send_feedback.js), los tests son [estos](app/serverless/test/send_feedback.test.js) y el despliegue está [aquí](https://amazing-villani-e2d732.netlify.app/.netlify/functions/send_feedback).

### Despliegue
El despliegue de estas funciones y el frontend lo he hecho en Netlify. Pese a que se puede hacer desde la UI, he configurado todo en [netlify.toml.](netlify.toml) En él especifico el directorio en el que implemento las funciones serverless, el directorio del frontend y las instrucciones de construcción.

He utilizado este servicio porque es un término medio entre cómodo y configurable. Me ha permitido incorporarlo a la estructura que ya tenía del proyecto con bastante facilidad, además del frontend. 

Finalmente, para probar también otro servicio, he implementado ambas funciones en [un repositorio aparte](https://github.com/AlexMenor/firebase-functions-que-vemos) para Firebase.
Se despliegan con [esta github action.](https://github.com/AlexMenor/firebase-functions-que-vemos/blob/master/.github/workflows/deploy.yml) 

[Esta es GetTrendingWatchables](https://us-central1-que-vemos.cloudfunctions.net/getTrendingWatchables) y [esta es SendFeedback.](https://us-central1-que-vemos.cloudfunctions.net/sendFeedback
)
