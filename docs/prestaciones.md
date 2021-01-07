# Pruebas de prestaciones

Uso gunicorn como gestor de procesos, usando como "worker" `uvicorn`, que es la manera recomendada [para ejecutar uvicorn en producción](https://www.uvicorn.org/#running-with-gunicorn).

He usado además JMeter para hacer pruebas de prestaciones en producción, usando distintos números de workers para ver cuál es el apropiado dado mi plan en heroku.

El escenario de prueba consiste en 10 usuarios haciendo peticiones de voto y resumen a dos sesiones distintas.

| Nº Workers | # Samples | Average | Median | 90% Line | 95% Line | 99% Line | Min | Max | Error % | Throughput | KB/sec |
| ---------- | --------- | ------- | ------ | -------- | -------- | -------- | --- | --- | ------- | ---------- | ------ |
| 1          | 160       | 296     | 256    | 457      | 532      | 668      | 165 | 708 | 0.00%   | 29.1       | 7.2    |
| 2          | 160       | 198     | 199    | 231      | 244      | 256      | 153 | 292 | 0.00%   | 39.1       | 9.7    |
| 4          | 160       | 191     | 191    | 220      | 225      | 239      | 139 | 258 | 0.00%   | 39.9       | 9.9    |
| **6**      | 160       | **187** | 191    | 214      | 219      | 227      | 148 | 237 | 0.00%   | **40.3**   | 10.0   |
| 8          | 160       | 209     | 211    | 248      | 255      | 309      | 153 | 348 | 0.00%   | 37.4       | 9.3    |
