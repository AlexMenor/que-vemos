# Despliegue en PaaS

He elegido heroku para desplegar mi microservicio:

- Aparte de ofrecer un plan gratuito, con el pack de Github se pueden conseguir créditos en la plataforma. He hecho uso de ellos para tener un plan Hobby que mantiene la aplicación despierta.
- Permite añadir "addons" como bases de datos, colas, etc... He usado redis de esta manera con mi microservicio.

## Configuración y despliegue automático

Cualquiera puede desplegar "Qué vemos" en heroku. Basta con:

- Hacer un fork
- Crear una aplicación en heroku
- Añadir al repositorio los secrets: `HEROKU_API_KEY` y `HEROKU_APP_NAME`.

Con esto, `git push` disparará [la pipeline CI/CD](../.github/workflows/ci-cd.yml), que después de (y solo después de) pasar los tests construye la imagen definida en [Dockerfile.web](../Dockerfile.web), la sube al registro de heroku y hace release. Todo esto usando la CLI de heroku y los secrets definidos arriba.

Se puede interactuar con el microservicio mediante la documentación de Swagger para probarlo [aquí](https://que-vemos.herokuapp.com/docs) y ver las operaciones disponibles.
