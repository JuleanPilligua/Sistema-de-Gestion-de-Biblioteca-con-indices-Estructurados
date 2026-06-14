from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, idUsuario, nombre, correo, contraseña):
        super().__init__(idUsuario, nombre, correo, contraseña)
        self.prestamosActivos = []

    def __str__(self):
        return f"[Cliente] ID: {self.idUsuario} | {self.nombre} (Préstamos activos: {len(self.prestamosActivos)})"

#Para ver o realizar prestamos el usuario lo hará mediante la logica del archivo logica.py, donde se gestionarán las operaciones relacionadas con los clientes y sus préstamos.