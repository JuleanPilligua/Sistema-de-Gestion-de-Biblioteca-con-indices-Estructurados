import datetime
from estructuras import ColaEspera

class Accion:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.timestamp = datetime.datetime.now()

    def deshacer(self, biblioteca):
        """Método abstracto para revertir la acción en la biblioteca."""
        raise NotImplementedError("Cada acción debe implementar su propio método para deshacerse.")


class AccionRegistroLibro(Accion):
    def __init__(self, libro):
        super().__init__(f"Registrado libro: '{libro.titulo}' ({libro.isbn})")
        self.isbn = libro.isbn

    def deshacer(self, biblioteca):
        eliminado = biblioteca.catalogo_libros.eliminar(self.isbn)
        if eliminado:
            return True, f"Deshecho: Se eliminó el libro '{eliminado.titulo}' registrado previamente."
        return False, "No se pudo deshacer el registro del libro."


class AccionRegistroUsuario(Accion):
    def __init__(self, usuario, rol):
        super().__init__(f"Registrado {rol}: '{usuario.nombre}' (ID: {usuario.idUsuario})")
        self.id_usuario = usuario.idUsuario

    def deshacer(self, biblioteca):
        eliminado = biblioteca.personas.eliminar_por_id(self.id_usuario)
        if eliminado:
            return True, f"Deshecho: Se eliminó el usuario '{eliminado.nombre}' registrado previamente."
        return False, "No se pudo deshacer el registro del usuario."


class AccionPrestamo(Accion):
    def __init__(self, libro, cliente, prestamo):
        super().__init__(f"Préstamo: '{libro.titulo}' a {cliente.nombre}")
        self.libro = libro
        self.cliente = cliente
        self.prestamo = prestamo

    def deshacer(self, biblioteca):
        self.libro.marcar_como_disponible()
        if self.prestamo in self.cliente.prestamosActivos:
            self.cliente.prestamosActivos.remove(self.prestamo)
        return True, f"Deshecho: Préstamo de '{self.libro.titulo}' a {self.cliente.nombre} cancelado."


class AccionColaEspera(Accion):
    def __init__(self, libro, cliente):
        super().__init__(f"Cola de espera: {cliente.nombre} para '{libro.titulo}'")
        self.isbn = libro.isbn
        self.id_cliente = cliente.idUsuario

    def deshacer(self, biblioteca):
        cola = biblioteca.colas_espera.get(self.isbn)
        persona = biblioteca.personas.buscar_por_id(self.id_cliente)
        
        if cola and persona:
            temp_lista = cola.obtener_lista()
            nueva_cola = ColaEspera()
            quitado = False
            for p in temp_lista:
                if p.idUsuario != self.id_cliente:
                    nueva_cola.encolar(p)
                else:
                    quitado = True
            biblioteca.colas_espera[self.isbn] = nueva_cola
            if quitado:
                return True, f"Deshecho: Se removió a {persona.nombre} de la cola de espera."
        return False, "No se pudo deshacer el registro en cola de espera."


class AccionDevolucion(Accion):
    def __init__(self, libro, cliente, prestamo_devuelto, siguiente_cliente=None, nuevo_prestamo=None):
        super().__init__(f"Devolución: '{libro.titulo}' por {cliente.nombre}")
        self.isbn = libro.isbn
        self.id_cliente = cliente.idUsuario
        self.prestamo_devuelto = prestamo_devuelto
        self.siguiente_cliente = siguiente_cliente
        self.nuevo_prestamo = nuevo_prestamo

    def deshacer(self, biblioteca):
        libro = biblioteca.catalogo_libros.buscar_por_isbn(self.isbn)
        persona = biblioteca.personas.buscar_por_id(self.id_cliente)

        if not libro or not persona:
            return False, "No se pudieron recuperar las entidades para deshacer la devolución."

        self.prestamo_devuelto.revertir_devolucion()
        persona.agregar_prestamo(self.prestamo_devuelto)

        # Si hubo préstamo automático al siguiente en cola, revertirlo
        if self.siguiente_cliente and self.nuevo_prestamo:
            if self.nuevo_prestamo in self.siguiente_cliente.prestamosActivos:
                self.siguiente_cliente.prestamosActivos.remove(self.nuevo_prestamo)
            
            # Volver a encolar al cliente al inicio de la cola
            cola = biblioteca.colas_espera.get(self.isbn)
            if not cola:
                cola = ColaEspera()
                biblioteca.colas_espera[self.isbn] = cola
            
            temp_lista = cola.obtener_lista()
            nueva_cola = ColaEspera()
            nueva_cola.encolar(self.siguiente_cliente)
            for p in temp_lista:
                nueva_cola.encolar(p)
            biblioteca.colas_espera[self.isbn] = nueva_cola

        libro.marcar_como_prestado()
        return True, f"Deshecho: Devolución de '{libro.titulo}' por {persona.nombre} cancelada. El libro vuelve a estar prestado."


class AccionEliminarLibro(Accion):
    def __init__(self, libro):
        super().__init__(f"Eliminado libro: '{libro.titulo}' ({libro.isbn})")
        self.libro = libro

    def deshacer(self, biblioteca):
        biblioteca.catalogo_libros.insertar(self.libro)
        return True, f"Deshecho: Se restauró el libro '{self.libro.titulo}' ({self.libro.isbn}) al catálogo."


class AccionLog(Accion):
    def __init__(self, descripcion):
        super().__init__(descripcion)

    def deshacer(self, biblioteca):
        return False, "Esta acción del historial (registro de actividad) no se puede deshacer."
