from .usuario import Usuario

class Bibliotecario(Usuario):
    def __init__(self, idUsuario, nombre, correo, contraseña, codigoEmpleado):
        super().__init__(idUsuario, nombre, correo, contraseña)
        self._codigoEmpleado = codigoEmpleado
    
    def __str__(self):
        return f"[Bibliotecario] ID: {self.idUsuario} | {self.nombre} (Código de Empleado: {self._codigoEmpleado})"