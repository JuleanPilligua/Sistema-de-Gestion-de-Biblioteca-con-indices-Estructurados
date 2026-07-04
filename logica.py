from modelos import Libro, Cliente, Bibliotecario, Prestamo
from estructuras import ArbolBinarioBusqueda, ListaEnlazadaPersonas, PilaHistorial, ColaEspera

class Accion:
    def __init__(self, descripcion):
        self.descripcion = descripcion

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


class GestionBiblioteca:
    def __init__(self):
        self.catalogo_libros = ArbolBinarioBusqueda()
        self.personas = ListaEnlazadaPersonas()
        self.historial = PilaHistorial()
        self.colas_espera = {}  # isbn -> ColaEspera

    def registrar_libro(self, isbn, titulo, autor):
        if self.catalogo_libros.buscar_por_isbn(isbn) is not None:
            return False, f"El libro con ISBN {isbn} ya está registrado."

        libro = Libro(isbn, titulo, autor)
        self.catalogo_libros.insertar(libro)
        self.historial.apilar(AccionRegistroLibro(libro))
        return True, f"Libro '{titulo}' registrado exitosamente."

    def registrar_usuario(self, idUsuario, nombre, correo, contraseña, rol, codigoEmpleado=None):
        if self.personas.buscar_por_id(idUsuario) is not None:
            return False, f"El usuario con ID {idUsuario} ya existe."
        if self.personas.buscar_por_correo(correo) is not None:
            return False, f"El usuario con correo {correo} ya existe."

        if rol.lower() == "bibliotecario":
            if not codigoEmpleado:
                return False, "Código de empleado es requerido para Bibliotecarios."
            usuario = Bibliotecario(idUsuario, nombre, correo, contraseña, codigoEmpleado)
        else:
            usuario = Cliente(idUsuario, nombre, correo, contraseña)

        self.personas.insertar(usuario)
        self.historial.apilar(AccionRegistroUsuario(usuario, rol))
        return True, f"{rol} '{nombre}' registrado exitosamente."

    def buscar_libro(self, criterio, valor):
        criterio = criterio.lower()
        if criterio == "isbn":
            res = self.catalogo_libros.buscar_por_isbn(valor)
            return [res] if res else []
        elif criterio == "titulo":
            return self.catalogo_libros.buscar_por_titulo(valor)
        elif criterio == "autor":
            return self.catalogo_libros.buscar_por_autor(valor)
        else:
            return []

    def realizar_prestamo(self, isbn, idCliente):
        libro = self.catalogo_libros.buscar_por_isbn(isbn)
        if not libro:
            return False, "El libro no existe en el catálogo."

        persona = self.personas.buscar_por_id(idCliente)
        if not persona:
            return False, "El cliente no está registrado."
        if not isinstance(persona, Cliente):
            return False, "El usuario indicado no es un Cliente."

        if libro.esta_disponible():
            libro.marcar_como_prestado()
            prestamo = Prestamo(libro, persona)
            persona.agregar_prestamo(prestamo)
            self.historial.apilar(AccionPrestamo(libro, persona, prestamo))
            return True, f"Préstamo realizado con éxito. Fecha límite: {prestamo.fecha_limite}"
        else:
            if isbn not in self.colas_espera:
                self.colas_espera[isbn] = ColaEspera()
            
            cola = self.colas_espera[isbn]
            if persona in cola.obtener_lista():
                return False, f"El cliente ya está en la cola de espera de este libro."
            
            if persona.tiene_prestamo_activo(isbn):
                return False, f"El cliente ya tiene prestado este libro actualmente."

            cola.encolar(persona)
            self.historial.apilar(AccionColaEspera(libro, persona))
            return True, f"El libro no está disponible. Se ha agregado a '{persona.nombre}' a la cola de espera (Lugar: {cola.tamanio})."

    def realizar_devolucion(self, isbn, idCliente):
        libro = self.catalogo_libros.buscar_por_isbn(isbn)
        if not libro:
            return False, "El libro no existe en el catálogo."

        persona = self.personas.buscar_por_id(idCliente)
        if not persona:
            return False, "El cliente no está registrado."
        if not isinstance(persona, Cliente):
            return False, "El usuario indicado no es un Cliente."

        prestamo_activo = persona.devolver_libro(isbn)
        if not prestamo_activo:
            return False, "El cliente no tiene un préstamo activo para este libro."

        msg_ret = f"Devolución de '{libro.titulo}' registrada con éxito."

        cola = self.colas_espera.get(isbn)
        siguiente_cliente = None
        nuevo_prestamo = None
        if cola and not cola.esta_vacia():
            siguiente_cliente = cola.desencolar()
            libro.marcar_como_prestado()
            nuevo_prestamo = Prestamo(libro, siguiente_cliente)
            siguiente_cliente.agregar_prestamo(nuevo_prestamo)
            msg_ret += f"\n[AUTOMÁTICO] El libro se prestó de inmediato a {siguiente_cliente.nombre} (siguiente en cola)."
        else:
            libro.marcar_como_disponible()

        self.historial.apilar(AccionDevolucion(libro, persona, prestamo_activo, siguiente_cliente, nuevo_prestamo))
        return True, msg_ret

    def deshacer_ultima_accion(self):
        if self.historial.esta_vacia():
            return False, "No hay acciones recientes para deshacer."

        accion = self.historial.desapilar()
        return accion.deshacer(self)

    def obtener_historial_operaciones(self, limite=10):
        acciones = self.historial.obtener_historial(limite)
        return [accion.descripcion for accion in acciones]

    def obtener_historial_prestamos_devoluciones(self):
        acciones = self.historial.obtener_historial(100)
        return [accion.descripcion for accion in acciones if isinstance(accion, (AccionPrestamo, AccionDevolucion))]

    def obtener_cola_de_espera(self, isbn):
        cola = self.colas_espera.get(isbn)
        if not cola or cola.esta_vacia():
            return []
        return [f"{cliente.nombre} (ID: {cliente.idUsuario})" for cliente in cola.obtener_lista()]

    def obtener_catalogo_ordenado(self):
        return self.catalogo_libros.obtener_inorden()