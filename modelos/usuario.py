class Usuario:
    def __init__(self, idUsuario, nombre, correo, contraseña):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña

    def __str__(self):
        return f"ID: {self.idUsuario}, Nombre: {self.nombre}"