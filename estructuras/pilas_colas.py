from collections import deque

class PilaHistorial:
    def __init__(self):
        self._items = deque()

    @property
    def tamanio(self):
        """Retorna el número de elementos en la pila."""
        return len(self._items)

    def apilar(self, accion):
        """Agrega una acción al tope de la pila."""
        self._items.append(accion)

    def desapilar(self):
        """Remueve y retorna la acción en el tope de la pila. Retorna None si está vacía."""
        if self.esta_vacia():
            return None
        return self._items.pop()

    def esta_vacia(self):
        """Retorna True si la pila no tiene elementos."""
        return len(self._items) == 0

    def vaciar(self):
        """Limpia todos los elementos del historial."""
        self._items.clear()

    def obtener_historial(self, limite=10):
        """Retorna una lista con las acciones más recientes (tope primero) hasta el límite indicado."""
        acciones = list(self._items)
        acciones.reverse()
        return acciones[:limite]


class ColaEspera:
    def __init__(self):
        self._items = deque()

    @property
    def tamanio(self):
        """Retorna el número de clientes en la cola."""
        return len(self._items)

    def encolar(self, cliente):
        """Agrega un cliente al final de la cola."""
        self._items.append(cliente)

    def desencolar(self):
        """Remueve y retorna al cliente al frente de la cola. Retorna None si está vacía."""
        if self.esta_vacia():
            return None
        return self._items.popleft()

    def esta_vacia(self):
        """Retorna True si la cola no tiene elementos."""
        return len(self._items) == 0

    def vaciar(self):
        """Limpia todos los elementos de la cola."""
        self._items.clear()

    def obtener_lista(self):
        """Retorna una lista ordenada con todos los clientes en cola (frente primero)."""
        return list(self._items)