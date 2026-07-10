from modelos import Libro, Cliente, Bibliotecario, Prestamo
from estructuras import ArbolBinarioBusqueda, ListaEnlazadaPersonas, PilaHistorial, ColaEspera
from acciones import (
    AccionRegistroLibro, AccionRegistroUsuario, AccionPrestamo,
    AccionColaEspera, AccionDevolucion, AccionEliminarLibro, AccionLog
)


class GestionBiblioteca:
    def __init__(self):
        self.catalogo_libros = ArbolBinarioBusqueda()
        self.personas = ListaEnlazadaPersonas()
        self.historiales = {}  # idUsuario -> PilaHistorial
        self.usuario_actual = None
        self.colas_espera = {}  # isbn -> ColaEspera

    @property
    def historial(self):
        if self.usuario_actual is not None:
            id_usuario = self.usuario_actual.idUsuario
        else:
            id_usuario = "_default"
        
        if id_usuario not in self.historiales:
            self.historiales[id_usuario] = PilaHistorial()
        return self.historiales[id_usuario]

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
        todas_acciones = []
        for hist in self.historiales.values():
            for accion in hist._items:
                if isinstance(accion, (AccionPrestamo, AccionDevolucion)):
                    todas_acciones.append(accion)
        todas_acciones.sort(key=lambda a: a.timestamp, reverse=True)
        return [accion.descripcion for accion in todas_acciones[:100]]

    def obtener_cola_de_espera(self, isbn):
        cola = self.colas_espera.get(isbn)
        if not cola or cola.esta_vacia():
            return []
        return [f"{cliente.nombre} (ID: {cliente.idUsuario})" for cliente in cola.obtener_lista()]

    def obtener_catalogo_ordenado(self):
        return self.catalogo_libros.obtener_inorden()