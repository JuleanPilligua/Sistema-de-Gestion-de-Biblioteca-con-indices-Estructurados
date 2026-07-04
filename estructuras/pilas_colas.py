class NodoPila:
    def __init__(self, accion):
        self.accion = accion
        self.siguiente = None


class PilaHistorial:
    def __init__(self):
        self.tope = None
        self.tamanio = 0

    def apilar(self, accion):
        nuevo_nodo = NodoPila(accion)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamanio += 1

    def desapilar(self):
        if self.esta_vacia():
            return None
        eliminado = self.tope.accion
        self.tope = self.tope.siguiente
        self.tamanio -= 1
        return eliminado

    def esta_vacia(self):
        return self.tope is None

    def obtener_historial(self, limite=10):
        acciones = []
        actual = self.tope
        while actual is not None and len(acciones) < limite:
            acciones.append(actual.accion)
            actual = actual.siguiente
        return acciones


class NodoCola:
    def __init__(self, cliente):
        self.cliente = cliente
        self.siguiente = None


class ColaEspera:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0

    def encolar(self, cliente):
        nuevo_nodo = NodoCola(cliente)
        if self.final is None:
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        eliminado = self.frente.cliente
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamanio -= 1
        return eliminado

    def esta_vacia(self):
        return self.frente is None

    def obtener_lista(self):
        clientes = []
        actual = self.frente
        while actual is not None:
            clientes.append(actual.cliente)
            actual = actual.siguiente
        return clientes