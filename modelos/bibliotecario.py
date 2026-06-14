from modelos.usuario import Usuario

class Bibliotecario(Usuario):
    def __init__(self, idUsuario, nombre, contraseña, codigoEmpleado):
        super().__init__(idUsuario, nombre, contraseña)
        self._codigoEmpleado = codigoEmpleado