class NodoLista:
    def __init__(self, persona):
        self.persona = persona
        self.siguiente = None


class ListaEnlazadaPersonas:
    def __init__(self):
        self.cabeza = None

    def insertar(self, persona):
        nuevo_nodo = NodoLista(persona)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def buscar_por_id(self, idUsuario):
        actual = self.cabeza
        while actual is not None:
            if actual.persona.idUsuario == idUsuario:
                return actual.persona
            actual = actual.siguiente
        return None

    def buscar_por_correo(self, correo):
        actual = self.cabeza
        while actual is not None:
            if actual.persona.correo.lower() == correo.lower():
                return actual.persona
            actual = actual.siguiente
        return None

    def eliminar_por_id(self, idUsuario):
        actual = self.cabeza
        anterior = None
        while actual is not None:
            if actual.persona.idUsuario == idUsuario:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return actual.persona
            anterior = actual
            actual = actual.siguiente
        return None

    def obtener_todos(self):
        personas = []
        actual = self.cabeza
        while actual is not None:
            personas.append(actual.persona)
            actual = actual.siguiente
        return personas