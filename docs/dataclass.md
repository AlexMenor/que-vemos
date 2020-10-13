# Dataclass, uso y justificación

`@dataclass` es un decorador de python que añade a una clase "estándar":

- Un constructor que inicializa todas sus propiedades. Por defecto.
- `__repr__()`, que computa la representación en string de un objeto de esa clase. Por defecto.
- `__eq__()`, para comparar igualdad entre objetos. La implementación compara una por una las propiedades de la clase. Por defecto.
- Métodos de comparación como `__lt__()` o `__ge__()`. Opcional.
- `__hash__()`. Opcional.
- Tira una excepción si alguna de sus propiedades se modifica. Opcional.

Lo pienso utilizar en clases sin comportamiento, ya que ahorran boilerplate y quedan más claras sus propiedades y tipos.
