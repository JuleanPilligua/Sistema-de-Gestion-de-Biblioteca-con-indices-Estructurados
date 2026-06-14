class Usuario:
    def __init__(self, idUsuario, nombre, contraseña):
        self._idUsuario = idUsuario
        self.nombre = nombre
        self._contraseña = contraseña

    def mostrarInfo(self):
        print(f"""
        ID Usuario: {self._idUsuario}
        Nombre: {self.nombre}
        """)