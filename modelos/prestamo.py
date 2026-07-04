import datetime

class Prestamo:
    def __init__(self, libro, cliente):
        self.libro = libro
        self.cliente = cliente
        self.fecha_salida = datetime.date.today()
        self.fecha_limite = self.fecha_salida + datetime.timedelta(days=14)
        self.devuelto = False

    def registrar_devolucion(self):
        """Registra la devolución del libro asociado al préstamo."""
        self.devuelto = True

    def revertir_devolucion(self):
        """Revierte el estado de devolución (vuelve a estar activo)."""
        self.devuelto = False

    def esta_activo(self):
        """Retorna True si el préstamo sigue activo (no devuelto)."""
        return not self.devuelto

    def __str__(self):
        estado = "Devuelto" if self.devuelto else "Activo"
        return f"Libro: '{self.libro.titulo}' | Vence: {self.fecha_limite} [{estado}]"