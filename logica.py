from modelos import Libro, Cliente, Bibliotecario, Prestamo
from estructuras import ArbolBinarioBusqueda, ListaEnlazadaPersonas, PilaHistorial, ColaEspera

class Accion:
    def __init__(self, tipo, descripcion, datos):
        self.tipo = tipo  # 'registro_libro', 'registro_usuario', 'prestamo', 'devolucion'
        self.descripcion = descripcion
        self.datos = datos


class GestionBiblioteca:
    def __init__(self):
        self.catalogo_libros = ArbolBinarioBusqueda()
        self.personas = ListaEnlazadaPersonas()
        self.historial = PilaHistorial()
        self.colas_espera = {}  # isbn -> ColaEspera

    def registrar_libro(self, isbn, titulo, autor):
        # Validar si ya existe
        if self.catalogo_libros.buscar_por_isbn(isbn) is not None:
            return False, f"El libro con ISBN {isbn} ya está registrado."

        libro = Libro(isbn, titulo, autor)
        self.catalogo_libros.insertar(libro)
        
        # Registrar en el historial
        accion = Accion(
            tipo='registro_libro',
            descripcion=f"Registrado libro: '{titulo}' ({isbn})",
            datos={'isbn': isbn}
        )
        self.historial.apilar(accion)
        return True, f"Libro '{titulo}' registrado exitosamente."

    def registrar_usuario(self, idUsuario, nombre, correo, contraseña, rol, codigoEmpleado=None):
        # Validar si ya existe
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
        
        # Registrar en el historial
        accion = Accion(
            tipo='registro_usuario',
            descripcion=f"Registrado {rol}: '{nombre}' (ID: {idUsuario})",
            datos={'idUsuario': idUsuario, 'rol': rol}
        )
        self.historial.apilar(accion)
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

        if libro.estado == "Disponible":
            libro.estado = "Prestado"
            prestamo = Prestamo(libro, persona)
            persona.prestamosActivos.append(prestamo)

            # Registrar en el historial
            accion = Accion(
                tipo='prestamo',
                descripcion=f"Préstamo: '{libro.titulo}' a {persona.nombre}",
                datos={'isbn': isbn, 'idCliente': idCliente, 'prestamo': prestamo}
            )
            self.historial.apilar(accion)
            return True, f"Préstamo realizado con éxito. Fecha límite: {prestamo.fecha_limite}"
        else:
            # Libro no disponible, gestionar cola de espera
            if isbn not in self.colas_espera:
                self.colas_espera[isbn] = ColaEspera()
            
            # Validar si ya está en la cola para no duplicar
            cola = self.colas_espera[isbn]
            if persona in cola.obtener_lista():
                return False, f"El cliente ya está en la cola de espera de este libro."
            
            # Validar si ya lo tiene prestado
            for p in persona.prestamosActivos:
                if p.libro.isbn == isbn:
                    return False, f"El cliente ya tiene prestado este libro actualmente."

            cola.encolar(persona)
            
            # Registrar en el historial
            accion = Accion(
                tipo='cola_espera',
                descripcion=f"Cola de espera: {persona.nombre} para '{libro.titulo}'",
                datos={'isbn': isbn, 'idCliente': idCliente}
            )
            self.historial.apilar(accion)
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

        # Buscar el préstamo activo
        prestamo_activo = None
        for p in persona.prestamosActivos:
            if p.libro.isbn == isbn:
                prestamo_activo = p
                break

        if not prestamo_activo:
            return False, "El cliente no tiene un préstamo activo para este libro."

        # Procesar devolución
        prestamo_activo.devuelto = True
        persona.prestamosActivos.remove(prestamo_activo)

        msg_ret = f"Devolución de '{libro.titulo}' registrada con éxito."

        # Verificar cola de espera
        cola = self.colas_espera.get(isbn)
        siguiente_cliente = None
        nuevo_prestamo = None
        if cola and not cola.esta_vacia():
            siguiente_cliente = cola.desencolar()
            libro.estado = "Prestado"
            nuevo_prestamo = Prestamo(libro, siguiente_cliente)
            siguiente_cliente.prestamosActivos.append(nuevo_prestamo)
            msg_ret += f"\n[AUTOMÁTICO] El libro se prestó de inmediato a {siguiente_cliente.nombre} (siguiente en cola)."
        else:
            libro.estado = "Disponible"

        # Registrar en el historial
        accion = Accion(
            tipo='devolucion',
            descripcion=f"Devolución: '{libro.titulo}' por {persona.nombre}",
            datos={
                'isbn': isbn,
                'idCliente': idCliente,
                'prestamo_devuelto': prestamo_activo,
                'siguiente_cliente': siguiente_cliente,
                'nuevo_prestamo': nuevo_prestamo
            }
        )
        self.historial.apilar(accion)
        return True, msg_ret

    def deshacer_ultima_accion(self):
        if self.historial.esta_vacia():
            return False, "No hay acciones recientes para deshacer."

        accion = self.historial.desapilar()
        tipo = accion.tipo
        datos = accion.datos

        if tipo == 'registro_libro':
            isbn = datos['isbn']
            eliminado = self.catalogo_libros.eliminar(isbn)
            if eliminado:
                return True, f"Deshecho: Se eliminó el libro '{eliminado.titulo}' registrado previamente."
            return False, "No se pudo deshacer el registro del libro."

        elif tipo == 'registro_usuario':
            idUsuario = datos['idUsuario']
            eliminado = self.personas.eliminar_por_id(idUsuario)
            if eliminado:
                return True, f"Deshecho: Se eliminó el usuario '{eliminado.nombre}' registrado previamente."
            return False, "No se pudo deshacer el registro del usuario."

        elif tipo == 'prestamo':
            isbn = datos['isbn']
            idCliente = datos['idCliente']
            prestamo = datos['prestamo']
            
            libro = self.catalogo_libros.buscar_por_isbn(isbn)
            persona = self.personas.buscar_por_id(idCliente)
            
            if libro and persona:
                libro.estado = "Disponible"
                if prestamo in persona.prestamosActivos:
                    persona.prestamosActivos.remove(prestamo)
                return True, f"Deshecho: Préstamo de '{libro.titulo}' a {persona.nombre} cancelado."
            return False, "No se pudo deshacer el préstamo."

        elif tipo == 'cola_espera':
            isbn = datos['isbn']
            idCliente = datos['idCliente']
            
            cola = self.colas_espera.get(isbn)
            persona = self.personas.buscar_por_id(idCliente)
            
            if cola and persona:
                # Quitar de la cola de espera recreando la cola sin este usuario
                temp_lista = cola.obtener_lista()
                nueva_cola = ColaEspera()
                quitado = False
                for p in temp_lista:
                    if p.idUsuario != idCliente:
                        nueva_cola.encolar(p)
                    else:
                        quitado = True
                self.colas_espera[isbn] = nueva_cola
                if quitado:
                    return True, f"Deshecho: Se removió a {persona.nombre} de la cola de espera."
            return False, "No se pudo deshacer el registro en cola de espera."

        elif tipo == 'devolucion':
            isbn = datos['isbn']
            idCliente = datos['idCliente']
            prestamo_devuelto = datos['prestamo_devuelto']
            siguiente_cliente = datos['siguiente_cliente']
            nuevo_prestamo = datos['nuevo_prestamo']

            libro = self.catalogo_libros.buscar_por_isbn(isbn)
            persona = self.personas.buscar_por_id(idCliente)

            if not libro or not persona:
                return False, "No se pudieron recuperar las entidades para deshacer la devolución."

            # Revertir devolución
            prestamo_devuelto.devuelto = False
            persona.prestamosActivos.append(prestamo_devuelto)

            # Revertir préstamo automático si ocurrió
            if siguiente_cliente and nuevo_prestamo:
                if nuevo_prestamo in siguiente_cliente.prestamosActivos:
                    siguiente_cliente.prestamosActivos.remove(nuevo_prestamo)
                # Volver a encolar al cliente al inicio de la cola
                cola = self.colas_espera.get(isbn)
                if not cola:
                    cola = ColaEspera()
                    self.colas_espera[isbn] = cola
                
                # Para ponerlo al frente, recreamos la cola poniendo a siguiente_cliente de primero
                temp_lista = cola.obtener_lista()
                nueva_cola = ColaEspera()
                nueva_cola.encolar(siguiente_cliente)
                for p in temp_lista:
                    nueva_cola.encolar(p)
                self.colas_espera[isbn] = nueva_cola

            libro.estado = "Prestado"
            return True, f"Deshecho: Devolución de '{libro.titulo}' por {persona.nombre} cancelada. El libro vuelve a estar prestado."

        elif tipo == 'eliminar_libro':
            libro = datos['libro']
            self.catalogo_libros.insertar(libro)
            return True, f"Deshecho: Se restauró el libro '{libro.titulo}' ({libro.isbn}) al catálogo."

        return False, "Tipo de acción desconocido para deshacer."

    def obtener_historial_operaciones(self, limite=10):
        acciones = self.historial.obtener_historial(limite)
        return [accion.descripcion for accion in acciones]

    def obtener_cola_de_espera(self, isbn):
        cola = self.colas_espera.get(isbn)
        if not cola or cola.esta_vacia():
            return []
        return [f"{cliente.nombre} (ID: {cliente.idUsuario})" for cliente in cola.obtener_lista()]

    def obtener_catalogo_ordenado(self):
        return self.catalogo_libros.obtener_inorden()