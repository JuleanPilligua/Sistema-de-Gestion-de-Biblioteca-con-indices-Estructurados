import datetime

class Prestamo:
    def __init__(self, libro, cliente):
        self.libro = libro
        self.cliente = cliente
        self.fecha_salida = datetime.date.today()
        self.fecha_limite = self.fecha_salida + datetime.timedelta(days=14)
        self.devuelto = False

    def __str__(self):
        estado = "Devuelto" if self.devuelto else "Activo"
        return f"Libro: '{self.libro.titulo}' | Vence: {self.fecha_limite} [{estado}]"