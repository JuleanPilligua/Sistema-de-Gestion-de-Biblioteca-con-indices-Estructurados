MANUAL DE USUARIO
Sistema de Gestión de Biblioteca con Índices Estructurados

Este manual contiene las instrucciones detalladas para el uso del sistema, tanto desde la interfaz de consola (CLI) como desde la interfaz gráfica de usuario (GUI).

---

1. INTRODUCCIÓN AL SISTEMA

El sistema cuenta con dos tipos de roles de usuario, cada uno con diferentes permisos y opciones de navegación:
•   Bibliotecario: Administrador del sistema. Tiene permisos para registrar y eliminar libros, registrar usuarios, realizar préstamos y devoluciones, visualizar listas de espera, deshacer operaciones erróneas y ver todo el historial del sistema.
•   Cliente: Usuario regular de la biblioteca. Puede buscar libros, solicitar préstamos, visualizar sus préstamos activos y ver el catálogo ordenado.

---

2. ACCESO AL SISTEMA (CREDENCIALES POR DEFECTO)

Al iniciar la aplicación, se cargan datos semilla automáticos para pruebas inmediatas. Las credenciales de acceso iniciales son:

•   Administrador / Bibliotecario por defecto:
    - Correo electrónico: admin@biblioteca.com
    - Contraseña: admin
    - Código de Empleado: EMP101

•   Clientes por defecto:
    - Correo electrónico: juan@correo.com | Contraseña: 123
    - Correo electrónico: maria@correo.com | Contraseña: 123
    - Correo electrónico: carlos@correo.com | Contraseña: 123

•   Libros por defecto en el catálogo:
    - ISBN: 9781 | Título: Cien años de soledad | Autor: Gabriel García Márquez
    - ISBN: 9782 | Título: Don Quijote de la Mancha | Autor: Miguel de Cervantes
    - ISBN: 9783 | Título: El Principito | Autor: Antoine de Saint-Exupéry
    - ISBN: 9784 | Título: Ficciones | Autor: Jorge Luis Borges

---

3. USO EN MODO CONSOLA (INTERFACE CLI)

Para navegar en la consola de comandos, el usuario debe digitar el número de la opción deseada y presionar la tecla Enter.

A. Menú de Inicio
•   Opción 1 - Iniciar Sesión: Permite ingresar el correo y la contraseña para acceder al menú correspondiente según el rol del usuario (Cliente o Bibliotecario).
•   Opción 2 - Registrarse: Permite crear una nueva cuenta de tipo Cliente ingresando cédula/ID, nombre completo, correo y contraseña.
•   Opción 3 - Salir: Cierra la ejecución del programa.

B. Menú de Cliente (Menú de Consultas)
Una vez iniciada la sesión como Cliente, el menú cuenta con las siguientes opciones:
•   Opción 1 - Buscar un libro específico: Permite buscar en el catálogo por ISBN, por Título o por Autor de forma precisa.
•   Opción 2 - Solicitar Préstamo de un libro: Solicita un libro ingresando su ISBN. Si el libro está disponible, el préstamo se registra de inmediato y se asigna una fecha de vencimiento (14 días después). Si no está disponible, el sistema lo agregará a la lista de espera del libro indicándole qué lugar de turno ocupa.
•   Opción 3 - Ver mis Préstamos Activos: Muestra la lista de libros que el cliente tiene en su posesión actualmente y su fecha de vencimiento.
•   Opción 4 - Mostrar todo el Catálogo Ordenado: Muestra todos los libros del catálogo ordenados numéricamente por su código ISBN.
•   Opción 5 - Volver al menú principal: Cierra la sesión del cliente actual.

C. Menú de Bibliotecario (Menú de Administración)
Una vez iniciada la sesión como Bibliotecario, se cuenta con las siguientes opciones:
•   Opción 1 - Registrar un Libro: Permite ingresar un nuevo ejemplar al catálogo solicitando ISBN, Título y Autor.
•   Opción 2 - Registrar un Usuario: Permite registrar un Cliente o un nuevo Bibliotecario (solicitando código de empleado obligatorio).
•   Opción 3 - Buscar un Libro: Búsqueda idéntica a la del menú del cliente.
•   Opción 4 - Registrar Préstamo: Registra un préstamo asociando el ISBN del libro y el ID del cliente.
•   Opción 5 - Registrar Devolución: Registra el retorno de un libro ingresando su ISBN y el ID del cliente. Si existían clientes en cola de espera para este libro, el sistema asignará el libro automáticamente al primer cliente de la fila.
•   Opción 6 - Ver Historial de Operaciones Recientes: Muestra las últimas acciones registradas en la biblioteca.
•   Opción 7 - Deshacer última operación: Revierte de forma inmediata la última acción de la pila del historial de operaciones (ej. si se prestó un libro por error, esta opción cancela el préstamo y devuelve el libro al catálogo).
•   Opción 8 - Ver cola de espera de un Libro: Permite consultar quiénes y en qué orden están esperando por un libro específico mediante su ISBN.
•   Opción 9 - Mostrar todo el Catálogo Ordenado: Listado completo de libros por ISBN.
•   Opción 10 - Eliminar un libro por ISBN: Permite borrar un libro del catálogo (solo si no está prestado actualmente).
•   Opción 11 - Mostrar todos los usuarios registrados: Muestra la lista de clientes y bibliotecarios registrados con sus respectivos ID y correo.
•   Opción 12 - Ver Historial de Préstamos y Devoluciones: Muestra un registro exclusivo de las transacciones de préstamos y devoluciones realizadas.
•   Opción 13 - Volver al menú principal: Cierra la sesión del administrador.

---

4. USO EN INTERFAZ GRÁFICA (GUI INTERACTIVA)

La interfaz gráfica ofrece un entorno web visualmente amigable e interactivo.

A. Login y Navegación
•   La pantalla de inicio cuenta con un panel para el ingreso de credenciales (correo y contraseña).
•   Un menú superior dinámico se adapta según el rol detectado tras el inicio de sesión.
•   Los formularios para registro de libros, usuarios, préstamos y devoluciones se procesan mediante diálogos y notificaciones en pantalla que confirman el éxito o error de cada transacción.

B. Visualizador de Estructuras (Panel Académico)
Esta es la sección principal para el análisis del comportamiento de las estructuras. En la interfaz gráfica verás diagramas interactivos de:
•   Visualizador del Catálogo (Árbol Binario de Búsqueda): Dibuja el árbol completo. Cada nodo representa un libro, mostrando visualmente las bifurcaciones a la izquierda y derecha. Al insertar un libro nuevo, verás cómo se crea un nuevo nodo y se conecta automáticamente en la posición que le corresponde según el orden binario del ISBN.
•   Visualizador de Usuarios (Lista Enlazada): Dibuja los usuarios registrados en una secuencia lineal conectados por flechas direccionales que representan los punteros.
•   Visualizador del Historial (Pila): Muestra las acciones como bloques apilados uno sobre otro. El bloque superior es la acción más reciente. Al dar clic en "Deshacer", verás cómo el bloque del tope desaparece y el sistema actualiza el resto de paneles reflejando el cambio.
•   Visualizador de Espera (Colas): Muestra los libros prestados que tienen clientes esperando, graficándolos en una fila india horizontal donde el primero de la fila es el siguiente en recibir el beneficio.

---

5. RESOLUCIÓN DE DUDAS OPERATIVAS COMUNES

•   ¿Qué pasa si un cliente solicita un libro agotado?
    El sistema no rechazará la solicitud, sino que agregará al cliente automáticamente a la cola de espera de ese libro. Cuando otro usuario devuelva el libro, el sistema detectará la cola de espera y asignará el libro al cliente en espera sin que el bibliotecario deba realizar un préstamo manual adicional.

•   ¿Cuántas acciones puedo deshacer?
    Puedes deshacer tantas operaciones como acciones tengas en la pila del historial transaccional de tu sesión actual. El botón "Deshacer" (Undo) irá desapilando los registros cronológicamente, uno por uno, hasta que la pila quede vacía.
