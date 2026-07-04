from .usuario import Usuario

class Bibliotecario(Usuario):
    def __init__(self, idUsuario, nombre, correo, contraseña, codigoEmpleado):
        super().__init__(idUsuario, nombre, correo, contraseña)
        self._codigoEmpleado = codigoEmpleado

    @property
    def codigo_empleado(self):
        """Getter para obtener el código de empleado del bibliotecario."""
        return self._codigoEmpleado

    @codigo_empleado.setter
    def codigo_empleado(self, nuevo_codigo):
        """Setter para actualizar el código de empleado con validación básica."""
        if not nuevo_codigo:
            raise ValueError("El código de empleado no puede estar vacío.")
        self._codigoEmpleado = nuevo_codigo

    def validar_codigo_empleado(self, codigo):
        """Verifica si el código proporcionado coincide con el del bibliotecario."""
        return self._codigoEmpleado == codigo
    
    def __str__(self):
        return f"[Bibliotecario] ID: {self.idUsuario} | {self.nombre} (Código de Empleado: {self._codigoEmpleado})"