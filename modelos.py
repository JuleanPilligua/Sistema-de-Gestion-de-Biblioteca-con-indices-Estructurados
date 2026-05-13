#Las clases Libros, Usuarios, Bibliotecario y Prestamos
class Libro:
    def __init__(self, idLibro, titulo, autor, genero, estado):
        self.idLibro = idLibro
        self.titulo = titulo
        self.autor = autor
        self.genero = []
        self.estado = estado

class Usuario:
    def __init__(self, idUsuario, nombre, correo, tipo, libros_prestados):
        self.__idUsuario = idUsuario
        self.nombre = nombre
        self._correo = correo
        self._libros_prestados = []