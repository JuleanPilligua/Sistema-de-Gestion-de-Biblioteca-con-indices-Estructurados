from logica import GestionBiblioteca
import cli

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

def main():
    biblioteca = GestionBiblioteca()
    inicializar_datos(biblioteca)
    cli.ejecutar_consola(biblioteca)

if __name__ == "__main__":
    main()