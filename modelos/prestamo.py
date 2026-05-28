from datetime import datetime
class Prestamo:
    def __init__(self, idPrestamo, idUsuario, titulo, fechaPrestamo, fechaDevolucion, estado):
        self._idPrestamo = idPrestamo
        self._idUsuario = idUsuario
        self.titulo = titulo
        self.fechaPrestamo = fechaPrestamo
        self.fechaDevolucion = fechaDevolucion
        self.estado = estado

    def finalizarPrestamo(self):
        self.estado = "devuelto"
        self.fechaDevolucion = datetime.now()
#Podriamos terminar haciendo que el estado sea un boleano, en ese caso el nombre de la variable cambiaría estaPrestado, y el valor por defecto es true, una vez que se llama al metodo "finalizarPrestamo", el estado pasaría a false

    def calcularDiasPrestamo(self):
        if self.estado == "devuelto":
            return (self.fechaDevolucion - self.fechaPrestamo).days
        else:
            print("El libro aún no ha sido devuelto.")

    def mostrarInfo(self):
        print(f"""
        Usuario: {self._idUsuario}
        Libro: {self.titulo}
        Estado: {self.estado}
        """)