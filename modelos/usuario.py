class Usuario:
    def __init__(self, idUsuario, nombre, correo, tipo, libros_prestados):
        self._idUsuario = idUsuario
        self.nombre = nombre
        self._correo = correo
        self._libros_prestados = []

    def agregarLibroPrestado(self, libro):
        self._libros_prestados.append(libro)

    def quitarLibroPrestado(self, libro):
        if libro in self._libros_prestados:
            self._libros_prestados.remove(libro)