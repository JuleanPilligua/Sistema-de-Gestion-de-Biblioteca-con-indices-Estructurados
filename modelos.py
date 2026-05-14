#Las clases Libros, Usuarios, Bibliotecario y Prestamos
class Libro:
    def __init__(self, isbn, titulo, autor, genero, estado):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = []
        self.estado = estado

    def actualizarEstado(self, nuevo_estado):
        self.estado = nuevo_estado

    def obtenerInformacion(self):
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Género: {', '.join(self.genero)}, Estado: {self.estado}"



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


class Bibliotecario:
    def __init__(self, idBibliotecario, nombre, correo):
        self._idBibliotecario = idBibliotecario
        self.nombre = nombre
        self._correo = correo



class Prestamo:
    def __init__(self, idPrestamo, idUsuario, isbn, fechaPrestamo, fechaDevolucion):
        self._idPrestamo = idPrestamo
        self._idUsuario = idUsuario
        self.isbn = isbn
        self.fechaPrestamo = fechaPrestamo
        self.fechaDevolucion = fechaDevolucion

    def calcularDiasRetraso(self, fechaActual):
        if self.fechaDevolucion < fechaActual:
            dias_retraso = (fechaActual - self.fechaDevolucion).days
            return dias_retraso
        else:
            return 0
        
    def finalizarPrestamo(self, fechaActual):
        dias_retraso = self.calcularDiasRetraso(fechaActual)
        if dias_retraso > 0:
            print(f"El préstamo tiene un retraso de {dias_retraso} días.")
        else:
            print("El préstamo se ha finalizado a tiempo.")