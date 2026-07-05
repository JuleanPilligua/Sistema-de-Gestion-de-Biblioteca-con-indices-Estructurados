import os
import sys
import webview
from logica import GestionBiblioteca
from acciones import AccionEliminarLibro, AccionLog
from main import inicializar_datos

class Api:
    def __init__(self):
        self.biblioteca = GestionBiblioteca()
        inicializar_datos(self.biblioteca)
        self.usuario_logueado = None

    def login(self, correo, contrasena):
        usuario = self.biblioteca.personas.buscar_por_correo(correo)
        if usuario and usuario.contraseña == contrasena:
            self.usuario_logueado = usuario
            self.biblioteca.usuario_actual = usuario
            role = "Bibliotecario" if hasattr(usuario, '_codigoEmpleado') else "Cliente"
            emp_code = usuario._codigoEmpleado if role == "Bibliotecario" else ""
            return {
                "success": True,
                "usuario": {
                    "idUsuario": usuario.idUsuario,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo,
                    "role": role,
                    "codigoEmpleado": emp_code
                }
            }
        return {"success": False, "message": "Correo o contraseña incorrectos."}

    def logout(self):
        self.usuario_logueado = None
        self.biblioteca.usuario_actual = None
        return {"success": True}

    def registrar_usuario(self, id_usuario, nombre, correo, contrasena, rol, cod_emp=None):
        exito, msg = self.biblioteca.registrar_usuario(id_usuario, nombre, correo, contrasena, rol, cod_emp)
        return {"success": exito, "message": msg}

    def registrar_libro(self, isbn, titulo, autor):
        exito, msg = self.biblioteca.registrar_libro(isbn, titulo, autor)
        return {"success": exito, "message": msg}

    def buscar_libro(self, criterio, valor):
        resultados = self.biblioteca.buscar_libro(criterio, valor)
        libros_list = []
        for libro in resultados:
            if libro:
                libros_list.append({
                    "isbn": libro.isbn,
                    "titulo": libro.titulo,
                    "autor": libro.autor,
                    "estado": libro.estado
                })
        return libros_list

    def realizar_prestamo(self, isbn, id_cliente):
        exito, msg = self.biblioteca.realizar_prestamo(isbn, id_cliente)
        return {"success": exito, "message": msg}

    def realizar_devolucion(self, isbn, id_cliente):
        exito, msg = self.biblioteca.realizar_devolucion(isbn, id_cliente)
        return {"success": exito, "message": msg}

    def obtener_historial_operaciones(self, limite=15):
        # Devuelve las descripciones del historial
        return self.biblioteca.obtener_historial_operaciones(limite)

    def obtener_historial_prestamos_devoluciones(self):
        # Devuelve el historial exclusivo de prestamos y devoluciones
        return self.biblioteca.obtener_historial_prestamos_devoluciones()

    def deshacer_ultima_accion(self):
        exito, msg = self.biblioteca.deshacer_ultima_accion()
        return {"success": exito, "message": msg}

    def obtener_cola_de_espera(self, isbn):
        return self.biblioteca.obtener_cola_de_espera(isbn)

    def obtener_catalogo_ordenado(self):
        libros = self.biblioteca.obtener_catalogo_ordenado()
        return [{
            "isbn": l.isbn,
            "titulo": l.titulo,
            "autor": l.autor,
            "estado": l.estado
        } for l in libros]

    def eliminar_libro(self, isbn):
        libro = self.biblioteca.catalogo_libros.buscar_por_isbn(isbn)
        if not libro:
            return {"success": False, "message": "El libro no existe en el catálogo."}
        if libro.estado == "Prestado":
            return {"success": False, "message": "No se puede eliminar el libro porque está prestado actualmente."}
        
        exito = self.biblioteca.catalogo_libros.eliminar(isbn)
        if exito:
            self.biblioteca.historial.apilar(AccionEliminarLibro(libro))
            return {"success": True, "message": f"Libro '{libro.titulo}' eliminado con éxito."}
        return {"success": False, "message": "Error al eliminar el libro."}

    def obtener_todos_usuarios(self):
        usuarios = self.biblioteca.personas.obtener_todos()
        ret = []
        for u in usuarios:
            role = "Bibliotecario" if hasattr(u, '_codigoEmpleado') else "Cliente"
            emp_code = u._codigoEmpleado if role == "Bibliotecario" else ""
            ret.append({
                "idUsuario": u.idUsuario,
                "nombre": u.nombre,
                "correo": u.correo,
                "role": role,
                "codigoEmpleado": emp_code,
                "prestamosActivosCount": len(u.prestamosActivos) if role == "Cliente" else 0
            })
        return ret

    def eliminar_usuario(self, id_usuario):
        usuario = self.biblioteca.personas.buscar_por_id(id_usuario)
        if not usuario:
            return {"success": False, "message": "El usuario no existe."}
        if self.usuario_logueado and self.usuario_logueado.idUsuario == id_usuario:
            return {"success": False, "message": "No puede eliminar su propio usuario activo."}
        if hasattr(usuario, 'prestamosActivos') and len(usuario.prestamosActivos) > 0:
            return {"success": False, "message": "No se puede eliminar el usuario porque tiene préstamos activos."}
        
        eliminado = self.biblioteca.personas.eliminar_por_id(id_usuario)
        if eliminado:
            role = "Bibliotecario" if hasattr(eliminado, '_codigoEmpleado') else "Cliente"
            self.biblioteca.historial.apilar(AccionLog(f"Eliminado {role}: '{eliminado.nombre}' (ID: {id_usuario})"))
            return {"success": True, "message": f"Usuario '{eliminado.nombre}' ({role}) eliminado con éxito."}
        return {"success": False, "message": "Error al intentar eliminar el usuario."}


    def obtener_prestamos_cliente(self, id_cliente):
        persona = self.biblioteca.personas.buscar_por_id(id_cliente)
        if not persona or not hasattr(persona, 'prestamosActivos'):
            return []
        
        prestamos_list = []
        for p in persona.prestamosActivos:
            prestamos_list.append({
                "isbn": p.libro.isbn,
                "titulo": p.libro.titulo,
                "autor": p.libro.autor,
                "fecha_salida": str(p.fecha_salida),
                "fecha_limite": str(p.fecha_limite),
                "devuelto": p.devuelto
            })
        return prestamos_list

    def obtener_arbol_estructura(self):
        # Retorna el árbol binario completo en formato jerárquico para graficarlo en el frontend
        def serializar_nodo(nodo):
            if nodo is None:
                return None
            return {
                "isbn": nodo.libro.isbn,
                "titulo": nodo.libro.titulo,
                "autor": nodo.libro.autor,
                "estado": nodo.libro.estado,
                "izquierdo": serializar_nodo(nodo.izquierdo),
                "derecho": serializar_nodo(nodo.derecho)
            }
        return serializar_nodo(self.biblioteca.catalogo_libros.raiz)

    def obtener_lista_estructura(self):
        # Retorna la lista enlazada de personas para graficarla
        usuarios = self.biblioteca.personas.obtener_todos()
        ret = []
        for u in usuarios:
            role = "Bibliotecario" if hasattr(u, '_codigoEmpleado') else "Cliente"
            ret.append({
                "idUsuario": u.idUsuario,
                "nombre": u.nombre,
                "correo": u.correo,
                "role": role
            })
        return ret

    def obtener_pila_estructura(self):
        # Retorna el historial completo con detalles de las acciones para graficar la pila
        acciones = self.biblioteca.historial.obtener_historial(30)
        return [acc.descripcion for acc in acciones]

    def obtener_todas_colas_estructura(self):
        # Retorna la cola de espera de todos los libros que tienen cola
        ret = {}
        for isbn, cola in self.biblioteca.colas_espera.items():
            if not cola.esta_vacia():
                libro = self.biblioteca.catalogo_libros.buscar_por_isbn(isbn)
                titulo = libro.titulo if libro else "Desconocido"
                ret[isbn] = {
                    "titulo": titulo,
                    "cola": [f"{cli.nombre} ({cli.idUsuario})" for cli in cola.obtener_lista()]
                }
        return ret

def main():
    api = Api()
    webview.create_window(
        title='Sistema de Gestión de Biblioteca - ULEAM',
        url='gui.html',
        js_api=api,
        width=1280,
        height=800,
        min_size=(1024, 700)
    )
    webview.start()

if __name__ == '__main__':
    main()
