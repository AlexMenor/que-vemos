## Logs
Dos módulos fundamentales:
- [LoggingMiddleware](app/middleware/logging.py): Importa un `handler` de [logging_config](app/config/logging_config.py) (que explico a continuación) 
y por cada petición entrante:
    - Genera un id único.
    - Imprime id, path y método.
    - Mide el tiempo que ha tardado en responder el servicio.
    - Imprime id, status code y tiempo de respuesta en milisegundos.
- [Logging config](app/config/logging_config.py): Construye el handler por el que se imprimirán los logs.
Si el modo de ejecución es `dev` los imprime por consola. Si el modo de ejecución es `prod` los imprime en `PAPERTRAIL`.
![logs](img/logs.png)

De nuevo hay un desacoplamiento de la implementación concreta, haciendo el servicio de logging intercambiable.
De nuevo hay un desacoplamiento de la implementación concreta, haciendo el servicio de logging intercambiable.
