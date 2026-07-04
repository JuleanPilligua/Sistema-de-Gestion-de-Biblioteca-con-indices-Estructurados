from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, idUsuario, nombre, correo, contraseña):
        super().__init__(idUsuario, nombre, correo, contraseña)
        self.prestamosActivos = []

    def tiene_prestamo_activo(self, isbn):
        """Verifica si el cliente ya tiene un préstamo activo del libro con el ISBN dado."""
        return any(p.libro.isbn == isbn for p in self.prestamosActivos)

    def agregar_prestamo(self, prestamo):
        """Asocia un préstamo activo al cliente."""
        self.prestamosActivos.append(prestamo)

    def buscar_prestamo_activo(self, isbn):
        """Busca y retorna el préstamo activo del libro con el ISBN dado. Retorna None si no existe."""
        for prestamo in self.prestamosActivos:
            if prestamo.libro.isbn == isbn:
                return prestamo
        return None

    def devolver_libro(self, isbn):
        """
        Registra la devolución del libro. Marca el préstamo como devuelto
        y lo remueve de la lista de préstamos activos del cliente.
        Retorna el préstamo devuelto o None si no tenía ese préstamo activo.
        """
        prestamo = self.buscar_prestamo_activo(isbn)
        if prestamo:
            prestamo.registrar_devolucion()
            self.prestamosActivos.remove(prestamo)
            return prestamo
        return None

    def __str__(self):
        return f"[Cliente] ID: {self.idUsuario} | {self.nombre} (Préstamos activos: {len(self.prestamosActivos)})"