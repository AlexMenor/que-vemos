# Implementación de persistencia (redis) y uso dentro del PaaS

Hasta ahora, la aplicación ya funcionaba en Heroku, pero con una implementación de [Session Store](../app/data/session_store/session_store.py) en [memoria](../app/data/session_store/in_memory_session_store.py).

Por tanto, las sesiones no sobrevivían a reinicios y no se podían utilizar múltiples instancias del microservicio.

## Implementación

[La implementación de Session Store en redis](../app/data/session_store/redis_session_store.py) soluciona este problema.

- Utiliza la biblioteca [aioredis](https://github.com/aio-libs/aioredis) como cliente de redis con interfaz asíncrona.
- Utiliza `pickle` para serializar y deserializar las estructuras de datos.
- Determina una fecha de expiración [configurable](configuracion.md). Las sesiones se utilizan y lo normal es que no se vuelvan a acceder a ellas, por lo que acaban expirando para liberar espacio.

Sin embargo, también ha introducido un problema:

- Existe una condición de carrera:

  1. Dos usuarios votan.
  2. Se obtiene la sesión dos veces.
  3. Se modifican las dos sesiones en memoria con los votos
  4. Se guardan las dos sesiones. Un voto se pierde.

- Para solucionarlo he usado la orden `setnx` de redis:

```python
async def get_one_and_lock(self, session_id: str) -> Session:
    acquired = 0

    while acquired == 0:
        acquired = await self.__redis.setnx(get_lock_name(session_id), 'true')
        if acquired == 0:
            # Devuelve el control al eventloop
            await asyncio.sleep(0)

    """ Si un proceso obtiene el lock y crashea, no pasa nada.
        El lock tiene expiración """
    await self.__redis.pexpire(get_lock_name(session_id), 100)

    return await self.get_one(session_id)
```

- Pone un "lock" a la sesión.
- Este lock se elimina cuando se guarda la sesión modificada o si pasan 100ms (eliminando la posibilidad de interbloqueo).
- Durante ese lock, si otra petición quiere modificar la misma sesión "espera" con `asyncio.sleep` sin bloquear otras peticiones.
- Esta función solo se usa si se va a modificar la sesión, si no, se utiliza `get_one` que no pone un lock a la sesión.

## Uso dentro del PaaS

Heroku permite añadir redis como "add-on". Al hacerlo, automáticamente se añade la variable de entorno REDIS_URL.

Sin embargo, podría utilizar cualquier otro servicio redis fuera del PaaS sin problema.
