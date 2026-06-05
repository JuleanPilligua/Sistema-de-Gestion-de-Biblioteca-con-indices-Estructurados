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