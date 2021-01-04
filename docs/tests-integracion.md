## Tests de integración

Pese a utilizar un framework asíncrono, FastAPI [provee un cliente de tests](https://fastapi.tiangolo.com/tutorial/testing/) basado en [requests](https://requests.readthedocs.io/en/master/)
que permite programar estos tests con funciones síncronas.
Además de este cliente, también he considerado [HTTPX](https://github.com/encode/httpx) en los que las funciones sí son asíncronas.

Finalmente me he decantado por el primero porque es más estable, porque no tengo funciones asíncronas en los tests de integración
y porque tiene un estilo más simple:

```python
# Requests
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

```python
# HTTPX
@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello world"}
```

De todas formas, más adelante en caso de necesitarlo podría utilizar `HTTPX` en unos tests y `requests` en otros.
De momento, `requests` hace lo que necesito, es más estable y tiene una interfaz más simple.

Los tests que he implementado son [estos](app/tests/integration/test_session_routes.py) y corresponden
a las historias de usuario que he comentado en la sección de rutas.

En cuanto a la implementación de los mismos, destacar las fixtures con `yield` que están soportadas
por `pytest` y me permiten utilizar la inyección de dependencias de FastAPI sin repetir en todos los tests setup y teardown.
