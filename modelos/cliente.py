from modelos.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, idUsuario, nombre, contraseña):
        super().__init__(idUsuario, nombre, contraseña)
        self._prestamosActivos = []

    def agregarPrestamo(self, prestamo):
        self._prestamosActivos.append(prestamo)

    def verPrestamos(self):
        if self._prestamosActivos:
            print("Prestamos activos:")
            for prestamo in self._prestamosActivos:
                print(f"- {prestamo.titulo}")
        else:
            print("No tienes libros prestados.")