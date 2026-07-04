import os
import sys
from logica import GestionBiblioteca
from modelos import Libro, Cliente, Bibliotecario, Prestamo

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione Enter para continuar...")

def solicitar_formulario(campos):
    """
    Solicita una serie de campos por consola.
    Retorna un diccionario con los valores o None si alguno obligatorio se deja vacío.
    """
    datos = {}
    for campo in campos:
        valor = input(f"{campo}: ").strip()
        if not valor:
            print(f"\nError: El campo '{campo}' es obligatorio.")
            return None
        datos[campo] = valor
    return datos


def inicializar_datos(biblioteca):
    # Registrar Bibliotecario por defecto
    biblioteca.registrar_usuario("L01", "Admin Biblioteca", "admin@biblioteca.com", "admin", "Bibliotecario", "EMP101")
    
    # Registrar Clientes por defecto
    biblioteca.registrar_usuario("C01", "Juan Pérez", "juan@correo.com", "123", "Cliente")
    biblioteca.registrar_usuario("C02", "María López", "maria@correo.com", "123", "Cliente")
    biblioteca.registrar_usuario("C03", "Carlos Mendoza", "carlos@correo.com", "123", "Cliente")
    
    # Registrar Libros por defecto
    biblioteca.registrar_libro("9781", "Cien años de soledad", "Gabriel García Márquez")
    biblioteca.registrar_libro("9782", "Don Quijote de la Mancha", "Miguel de Cervantes")
    biblioteca.registrar_libro("9783", "El Principito", "Antoine de Saint-Exupéry")
    biblioteca.registrar_libro("9784", "Ficciones", "Jorge Luis Borges")
    
    # Vaciar el historial inicial para que las acciones de inicialización no llenen la pila del usuario
    biblioteca.historial.vaciar()

def menu_cliente(biblioteca, cliente_logueado):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print(f"      [ MENÚ DE CONSULTAS - CLIENTE: {cliente_logueado.nombre.upper()} ]")
        print("=" * 60)
        print("1. Buscar un Libro específico")
        print("2. Solicitar Préstamo de un Libro")
        print("3. Ver mis Préstamos Activos")
        print("4. Mostrar todo el Catálogo Ordenado")
        print("5. Volver al menú principal")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- BUSCAR LIBRO ---")
            print("1. Buscar por ISBN")
            print("2. Buscar por Título")
            print("3. Buscar por Autor")
            criterio_op = input("Seleccione criterio: ").strip()
            
            criterio = ""
            if criterio_op == "1":
                criterio = "isbn"
            elif criterio_op == "2":
                criterio = "titulo"
            elif criterio_op == "3":
                criterio = "autor"
            else:
                print("Opción inválida.")
                pausar()
                continue
                
            valor = input(f"Ingrese el valor a buscar ({criterio}): ").strip()
            resultados = biblioteca.buscar_libro(criterio, valor)
            
            print("\nResultados encontrados:")
            if resultados and any(resultados):
                for libro in resultados:
                    if libro:
                        print(f"- {libro}")
            else:
                print("No se encontraron libros.")
            pausar()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- SOLICITAR PRÉSTAMO ---")
            isbn = input("Ingrese el ISBN del libro que desea: ").strip()
            if isbn:
                exito, msg = biblioteca.realizar_prestamo(isbn, cliente_logueado.idUsuario)
                print(f"\nResultado: {msg}")
            else:
                print("ISBN no puede estar vacío.")
            pausar()
            
        elif opcion == "3":
            limpiar_pantalla()
            print(f"--- PRÉSTAMOS ACTIVOS DE {cliente_logueado.nombre.upper()} ---")
            if not cliente_logueado.prestamosActivos:
                print("No tiene préstamos activos.")
            else:
                for idx, prestamo in enumerate(cliente_logueado.prestamosActivos, 1):
                    print(f"{idx}. {prestamo}")
            pausar()
            
        elif opcion == "4":
            limpiar_pantalla()
            print("--- CATÁLOGO ORDENADO DE LIBROS (RECORRIDO INORDEN) ---")
            libros = biblioteca.obtener_catalogo_ordenado()
            if not libros:
                print("No hay libros en el catálogo.")
            else:
                for libro in libros:
                    print(f"- {libro}")
            pausar()
            
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            pausar()

def menu_bibliotecario(biblioteca, bibliotecario_logueado):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print(f"   [ MENÚ DE ADMINISTRACIÓN - BIBLIOTECARIO: {bibliotecario_logueado.nombre.upper()} ]")
        print("=" * 60)
        print("1. Registrar un Libro")
        print("2. Registrar un Usuario (Cliente o Bibliotecario)")
        print("3. Buscar un Libro")
        print("4. Registrar Préstamo de un Libro")
        print("5. Registrar Devolución de un Libro")
        print("6. Ver Historial de Operaciones Recientes")
        print("7. Deshacer última operación (Pila)")
        print("8. Ver cola de espera de un Libro")
        print("9. Mostrar todo el Catálogo Ordenado (Recorrido Inorden)")
        print("10. Eliminar un libro por ISBN")
        print("11. Mostrar todos los usuarios registrados")
        print("12. Ver Historial de Préstamos y Devoluciones")
        print("13. Volver al menú principal")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- REGISTRAR NUEVO LIBRO ---")
            datos = solicitar_formulario(["ISBN del libro", "Título del libro", "Autor del libro"])
            if datos:
                exito, msg = biblioteca.registrar_libro(datos["ISBN del libro"], datos["Título del libro"], datos["Autor del libro"])
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- REGISTRAR NUEVO USUARIO ---")
            datos = solicitar_formulario(["ID de Usuario", "Nombre completo", "Correo electrónico", "Contraseña"])
            if datos:
                print("Seleccione rol:\n1. Cliente\n2. Bibliotecario")
                rol_op = input("Opción: ").strip()
                
                if rol_op == "1":
                    rol = "Cliente"
                    cod_emp = None
                elif rol_op == "2":
                    rol = "Bibliotecario"
                    cod_emp = input("Código de Empleado: ").strip()
                    if not cod_emp:
                        print("Error: El código de empleado es obligatorio para Bibliotecarios.")
                        pausar()
                        continue
                else:
                    print("Rol inválido.")
                    pausar()
                    continue
                    
                exito, msg = biblioteca.registrar_usuario(
                    datos["ID de Usuario"], datos["Nombre completo"], 
                    datos["Correo electrónico"], datos["Contraseña"], rol, cod_emp
                )
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "3":
            limpiar_pantalla()
            print("--- BUSCAR LIBRO ---")
            print("1. Buscar por ISBN")
            print("2. Buscar por Título")
            print("3. Buscar por Autor")
            criterio_op = input("Seleccione criterio: ").strip()
            
            criterio = ""
            if criterio_op == "1":
                criterio = "isbn"
            elif criterio_op == "2":
                criterio = "titulo"
            elif criterio_op == "3":
                criterio = "autor"
            else:
                print("Opción inválida.")
                pausar()
                continue
                
            valor = input(f"Ingrese el valor a buscar ({criterio}): ").strip()
            resultados = biblioteca.buscar_libro(criterio, valor)
            
            print("\nResultados encontrados:")
            if resultados and any(resultados):
                for libro in resultados:
                    if libro:
                        print(f"- {libro}")
            else:
                print("No se encontraron libros.")
            pausar()
            
        elif opcion == "4":
            limpiar_pantalla()
            print("--- REGISTRAR PRÉSTAMO ---")
            datos = solicitar_formulario(["ISBN del libro", "ID del Cliente"])
            if datos:
                exito, msg = biblioteca.realizar_prestamo(datos["ISBN del libro"], datos["ID del Cliente"])
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "5":
            limpiar_pantalla()
            print("--- REGISTRAR DEVOLUCIÓN ---")
            datos = solicitar_formulario(["ISBN del libro", "ID del Cliente"])
            if datos:
                exito, msg = biblioteca.realizar_devolucion(datos["ISBN del libro"], datos["ID del Cliente"])
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "6":
            limpiar_pantalla()
            print("--- HISTORIAL DE OPERACIONES RECIENTES (PILA) ---")
            historial = biblioteca.obtener_historial_operaciones(15)
            if not historial:
                print("No hay operaciones en el historial.")
            else:
                for idx, desc in enumerate(historial, 1):
                    print(f"{idx}. {desc}")
            pausar()
            
        elif opcion == "7":
            limpiar_pantalla()
            print("--- DESHACER ÚLTIMA OPERACIÓN ---")
            exito, msg = biblioteca.deshacer_ultima_accion()
            print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "8":
            limpiar_pantalla()
            print("--- VER COLA DE ESPERA POR LIBRO ---")
            isbn = input("ISBN del libro: ").strip()
            if not isbn:
                print("ISBN no puede estar vacío.")
            else:
                libro = biblioteca.catalogo_libros.buscar_por_isbn(isbn)
                if not libro:
                    print("El libro no existe.")
                else:
                    print(f"\nLibro: {libro}")
                    cola = biblioteca.obtener_cola_de_espera(isbn)
                    if not cola:
                        print("No hay clientes en la cola de espera de este libro.")
                    else:
                        print("Clientes en espera:")
                        for pos, cli in enumerate(cola, 1):
                            print(f" {pos}. {cli}")
            pausar()
            
        elif opcion == "9":
            limpiar_pantalla()
            print("--- CATÁLOGO ORDENADO DE LIBROS (RECORRIDO INORDEN) ---")
            libros = biblioteca.obtener_catalogo_ordenado()
            if not libros:
                print("No hay libros en el catálogo.")
            else:
                for libro in libros:
                    print(f"- {libro}")
            pausar()
            
        elif opcion == "10":
            limpiar_pantalla()
            print("--- ELIMINAR LIBRO DEL CATÁLOGO ---")
            isbn = input("ISBN del libro a eliminar: ").strip()
            if not isbn:
                print("Error: El ISBN es obligatorio.")
            else:
                libro = biblioteca.catalogo_libros.buscar_por_isbn(isbn)
                if not libro:
                    print("Error: El libro no existe en el catálogo.")
                elif not libro.esta_disponible():
                    print("Error: No se puede eliminar el libro porque está prestado actualmente.")
                else:
                    exito = biblioteca.catalogo_libros.eliminar(isbn)
                    if exito:
                        from logica import AccionEliminarLibro
                        biblioteca.historial.apilar(AccionEliminarLibro(libro))
                        print(f"Libro '{libro.titulo}' eliminado con éxito.")
                    else:
                        print("Error inesperado al intentar eliminar el libro.")
            pausar()

        elif opcion == "11":
            limpiar_pantalla()
            print("--- USUARIOS REGISTRADOS EN EL SISTEMA (LISTA ENLAZADA) ---")
            usuarios = biblioteca.personas.obtener_todos()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                for u in usuarios:
                    print(f"- {u}")
            pausar()
            
        elif opcion == "12":
            limpiar_pantalla()
            print("--- HISTORIAL DE PRÉSTAMOS Y DEVOLUCIONES ---")
            historial = biblioteca.obtener_historial_prestamos_devoluciones()
            if not historial:
                print("No hay préstamos ni devoluciones registrados en el historial.")
            else:
                for idx, desc in enumerate(historial, 1):
                    print(f"{idx}. {desc}")
            pausar()
            
        elif opcion == "13":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            pausar()

def main():
    biblioteca = GestionBiblioteca()
    inicializar_datos(biblioteca)
    
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("      SISTEMA DE GESTIÓN DE BIBLIOTECA ESTRUCTURADO")
        print("=" * 60)
        print("1. Iniciar Sesión")
        print("2. Registrarse (Crear cuenta de Cliente)")
        print("3. Salir")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- INICIAR SESIÓN ---")
            datos = solicitar_formulario(["Correo electrónico", "Contraseña"])
            if datos:
                usuario = biblioteca.personas.buscar_por_correo(datos["Correo electrónico"])
                if usuario and usuario.verificar_contraseña(datos["Contraseña"]):
                    if isinstance(usuario, Bibliotecario):
                        menu_bibliotecario(biblioteca, usuario)
                    elif isinstance(usuario, Cliente):
                        menu_cliente(biblioteca, usuario)
                    else:
                        print("Error de rol desconocido.")
                        pausar()
                else:
                    print("Correo o contraseña incorrectos.")
                    pausar()
                
        elif opcion == "2":
            limpiar_pantalla()
            print("--- REGISTRO DE NUEVO CLIENTE ---")
            datos = solicitar_formulario(["Cédula / ID", "Nombre completo", "Correo electrónico", "Contraseña"])
            if datos:
                exito, msg = biblioteca.registrar_usuario(
                    datos["Cédula / ID"], datos["Nombre completo"], 
                    datos["Correo electrónico"], datos["Contraseña"], "Cliente"
                )
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "3":
            print("\n¡Gracias por utilizar el sistema de biblioteca!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            pausar()

if __name__ == "__main__":
    main()