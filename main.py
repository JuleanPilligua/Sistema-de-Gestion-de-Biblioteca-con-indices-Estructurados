import os
import sys
from logica import GestionBiblioteca
from modelos import Libro, Cliente, Bibliotecario, Prestamo

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione Enter para continuar...")

def mostrar_analisis_complejidad():
    limpiar_pantalla()
    print("=" * 75)
    print("       ANÁLISIS COMPARATIVO DE COMPLEJIDAD DE LAS OPERACIONES")
    print("=" * 75)
    print(f"{'Estructura / Operación':<35} | {'Caso Promedio':<15} | {'Peor Caso':<15}")
    print("-" * 75)
    print(f"{'Árbol BST (Inserción por ISBN)':<35} | {'O(log n)':<15} | {'O(n)':<15}")
    print(f"{'Árbol BST (Búsqueda por ISBN)':<35} | {'O(log n)':<15} | {'O(n)':<15}")
    print(f"{'Árbol BST (Búsqueda por Título/Autor)':<35} | {'O(n)':<15} | {'O(n)':<15}")
    print(f"{'Árbol BST (Eliminación por ISBN)':<35} | {'O(log n)':<15} | {'O(n)':<15}")
    print(f"{'Lista Enlazada (Inserción al final)':<35} | {'O(n)':<15} | {'O(n)':<15}")
    print(f"{'Lista Enlazada (Búsqueda/Elim. ID)':<35} | {'O(n)':<15} | {'O(n)':<15}")
    print(f"{'Pila Historial (Apilar/Desapilar)':<35} | {'O(1)':<15} | {'O(1)':<15}")
    print(f"{'Cola de Espera (Encolar/Desencolar)':<35} | {'O(1)':<15} | {'O(1)':<15}")
    print("=" * 75)
    print("Explicaciones Técnicas:")
    print("1. Árbol Binario de Búsqueda (BST) para Libros:")
    print("   - Indexar y buscar por ISBN es rápido O(log n) porque aprovechamos el orden del árbol.")
    print("   - Si el árbol se desbalancea (por ejemplo, al insertar claves ordenadas), degenera en")
    print("     una lista enlazada, por lo que el peor caso es O(n).")
    print("   - Buscar por Título o Autor requiere recorrer todo el árbol (Inorden), lo que es O(n).")
    print("2. Lista Enlazada para Usuarios:")
    print("   - La inserción al final requiere recorrer la lista hasta el último nodo: O(n).")
    print("   - La búsqueda y eliminación por ID requieren una búsqueda secuencial de O(n) pasos.")
    print("3. Pila y Cola (Historial y Espera):")
    print("   - Se realizan adiciones/extracciones solo en los extremos (tope o frente/final),")
    print("     lo que no depende de la cantidad de elementos, siendo siempre O(1).")
    print("=" * 75)
    pausar()

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
    biblioteca.historial.tope = None
    biblioteca.historial.tamanio = 0

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
            exito, msg = biblioteca.realizar_prestamo(isbn, cliente_logueado.idUsuario)
            print(f"\nResultado: {msg}")
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
        print("12. Volver al menú principal")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- REGISTRAR NUEVO LIBRO ---")
            isbn = input("ISBN del libro: ").strip()
            titulo = input("Título del libro: ").strip()
            autor = input("Autor del libro: ").strip()
            if not isbn or not titulo or not autor:
                print("Error: Todos los campos son obligatorios.")
            else:
                exito, msg = biblioteca.registrar_libro(isbn, titulo, autor)
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- REGISTRAR NUEVO USUARIO ---")
            id_usuario = input("ID de Usuario: ").strip()
            nombre = input("Nombre completo: ").strip()
            correo = input("Correo electrónico: ").strip()
            contraseña = input("Contraseña: ").strip()
            print("Seleccione rol:\n1. Cliente\n2. Bibliotecario")
            rol_op = input("Opción: ").strip()
            
            if rol_op == "1":
                rol = "Cliente"
                cod_emp = None
            elif rol_op == "2":
                rol = "Bibliotecario"
                cod_emp = input("Código de Empleado: ").strip()
            else:
                print("Rol inválido.")
                pausar()
                continue
                
            if not id_usuario or not nombre or not correo or not contraseña:
                print("Error: Todos los campos obligatorios deben completarse.")
            else:
                exito, msg = biblioteca.registrar_usuario(id_usuario, nombre, correo, contraseña, rol, cod_emp)
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
            isbn = input("ISBN del libro: ").strip()
            id_cliente = input("ID del Cliente: ").strip()
            if not isbn or not id_cliente:
                print("Error: Todos los campos son obligatorios.")
            else:
                exito, msg = biblioteca.realizar_prestamo(isbn, id_cliente)
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "5":
            limpiar_pantalla()
            print("--- REGISTRAR DEVOLUCIÓN ---")
            isbn = input("ISBN del libro: ").strip()
            id_cliente = input("ID del Cliente: ").strip()
            if not isbn or not id_cliente:
                print("Error: Todos los campos son obligatorios.")
            else:
                exito, msg = biblioteca.realizar_devolucion(isbn, id_cliente)
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
                elif libro.estado == "Prestado":
                    print("Error: No se puede eliminar el libro porque está prestado actualmente.")
                else:
                    exito = biblioteca.catalogo_libros.eliminar(isbn)
                    if exito:
                        # Registrar en el historial
                        from logica import Accion
                        biblioteca.historial.apilar(Accion('eliminar_libro', f"Eliminado libro: '{libro.titulo}' ({isbn})", {'libro': libro}))
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
        print("3. Ver Análisis de Complejidad de Estructuras")
        print("4. Salir")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- INICIAR SESIÓN ---")
            correo = input("Correo electrónico: ").strip()
            contraseña = input("Contraseña: ").strip()
            
            usuario = biblioteca.personas.buscar_por_correo(correo)
            if usuario and usuario.contraseña == contraseña:
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
            id_usuario = input("Cédula / ID: ").strip()
            nombre = input("Nombre completo: ").strip()
            correo = input("Correo electrónico: ").strip()
            contraseña = input("Contraseña: ").strip()
            
            if not id_usuario or not nombre or not correo or not contraseña:
                print("Error: Todos los campos son obligatorios.")
            else:
                exito, msg = biblioteca.registrar_usuario(id_usuario, nombre, correo, contraseña, "Cliente")
                print(f"\nResultado: {msg}")
            pausar()
            
        elif opcion == "3":
            mostrar_analisis_complejidad()
            
        elif opcion == "4":
            print("\n¡Gracias por utilizar el sistema de biblioteca!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            pausar()

if __name__ == "__main__":
    main()