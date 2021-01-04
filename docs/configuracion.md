## Configuración

En el módulo [config](app/config/config.py) está toda la configuración de la aplicación.

- Desde otros módulos se puede importar `config` (que no es más que un diccionario) y la constante a utilizar.
  Por ejemplo, en la configuración de los logs:

```python
handler = SysLogHandler(address=(config[PAPERTRAIL_HOST], int(config[PAPERTRAIL_PORT])))

# (PAPERTRAIL_HOST, PAPERTRAIL_PORT están declaradas así)
PAPERTRAIL_HOST = 'PAPERTRAIL_HOST'
PAPERTRAIL_PORT = 'PAPERTRAIL_PORT'
#Al declararlas así no hay posibilidad de equivocarse al usarlas.

config['PAPERTRAIL_POST'] # Así sí me puedo equivocar

```

- En primer lugar se intentan obtener las variables de `etcd`.
- Si falla, usamos `dotenv` para tomarlas de un `.env` o del entorno si este no existe.
- Por último, se verifica la configuración:
  - Si el modo es producción deben estar todas las variables inicializadas.
  - Si el modo es desarrollo, todas deben estar inicializadas excepto la `PAPERTRAIL_*` y `REDIS_*` que explicaré más adelante.
  - Se lanza una excepción si falla esta verificación.

Los tests de este módulo se pueden ver [aquí](app/tests/unit/test_config.py).

Las variables declaradas hasta el momento son:

- MODE: Si se está ejecutando la aplicación en desarrollo o en producción. Más abajo lo explico en detalle.
- NUM_OF_WATCHABLES_PER_SESSION: Cuántos watchables se votarán en cada sesión.
- MAX_USERS_PER_SESSION: Cuántos usuarios máximos admite cada sesión.
- PAPERTRAIL_HOST y PAPERTRAIL_PORT: Configuración de papertrail.
- REDIS_URL
- REDIS_EXPIRATION: Determina cuántos segundos se mantiene en la base de datos una clave de redis que no se haya utilizado más.

`REDIS_*` solo se utilizan si el modo es `prod`.
