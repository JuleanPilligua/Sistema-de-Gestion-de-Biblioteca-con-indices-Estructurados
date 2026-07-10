MANUAL DE USUARIO
Sistema de Gestión de Biblioteca con Índices Estructurados

Este manual contiene las instrucciones detalladas para el uso del sistema a través de su interfaz gráfica web (GUI).

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

3. NAVEGACIÓN Y ACCESO EN LA INTERFAZ WEB

El sistema ofrece una experiencia visual interactiva adaptada para su navegación en entorno web.

A. Login y Registro
•   Iniciar Sesión: Ingrese el correo electrónico y contraseña. El sistema redirigirá al portal del rol correspondiente (Cliente o Bibliotecario).
•   Registrarse: Pestaña disponible para que los usuarios puedan registrarse como Clientes suministrando Cédula/ID, Nombre completo, Correo electrónico y Contraseña.

B. Menú Lateral (Sidebar)
Permite alternar entre las diferentes secciones y herramientas habilitadas según el perfil actual:
•   Dashboard (Ambos): Contiene tarjetas estadísticas clave del sistema y el historial de acciones recientes.
•   Catálogo de Libros (Ambos): Acceso a la búsqueda del catálogo mediante filtros.
•   Mis Préstamos (Cliente): Sección para comprobar las fechas límite y el estado de sus préstamos.
•   Usuarios (Bibliotecario): Permite visualizar todos los usuarios registrados, así como registrar o eliminar cuentas.
•   Catálogo Visual (Bibliotecario): Gráfico del catálogo interactivo en forma de árbol.
•   Historial Préstamos (Bibliotecario): Reporte histórico global de préstamos y devoluciones.

---

4. OPERACIONES DE ROL CLIENTE

A. Búsqueda y Préstamos (Sección Catálogo de Libros)
•   Buscar Libros: Utilice la barra de búsqueda y el selector de criterio para filtrar libros por Título, ISBN o Autor.
•   Solicitar Préstamos: Si la tarjeta de un libro indica estado "Disponible", haga clic en "Solicitar Préstamo". El libro se le asignará y se establecerá una fecha de vencimiento a los 14 días.
•   Entrar a Lista de Espera: Si el libro está "Prestado", se habilita el botón "Unirse a Lista de Espera". Esto lo añadirá a la cola de espera de ese libro.

B. Control de Préstamos Activos (Sección Mis Préstamos)
•   Muestra sus préstamos en formato de lista con información detallada de ISBN, Título, Fecha de salida, Fecha límite de retorno y el Estado del préstamo.

---

5. OPERACIONES DE ROL BIBLIOTECARIO

A. Dashboard y Panel de Control
•   Estadísticas: Monitoree en tiempo real la cantidad de libros, usuarios, préstamos activos y cantidad de acciones.
•   Acciones Rápidas: Botones directos para abrir ventanas de registro rápido de libros y usuarios.
•   Historial de Operaciones Recientes: Muestra de forma cronológica (pila) las acciones registradas en el sistema.
•   Deshacer Última Acción (Undo): Ubicado al lado del historial, este botón permite revertir cronológicamente la última acción efectuada (inserciones, eliminaciones, préstamos o devoluciones).

B. Gestión del Catálogo (Sección Catálogo de Libros)
•   Insertar Libro: Utilice el botón "Nuevo Libro" para registrar un nuevo ejemplar ingresando ISBN, Título y Autor.
•   Prestar/Devolución: El botón interactivo de la tarjeta de cada libro cambia según su estado:
    - Prestar (Disponible): Abre un diálogo para ingresar el ID del cliente al cual se le asignará el libro.
    - Devolución (Prestado): Registra la entrega de vuelta del libro. Si había clientes esperando en la cola del libro, el sistema asignará el libro automáticamente al primer cliente de la fila.
•   Eliminar Libro: Botón "Eliminar" en cada tarjeta para remover ejemplares que no tengan préstamos activos.

C. Gestión de Usuarios (Sección Usuarios)
•   Visualización: Detalla en una tabla el ID, Nombre completo, Correo, Rol, Código de Empleado y número de préstamos activos de todos los usuarios.
•   Registrar Nuevo Usuario: Formulario para añadir nuevos Clientes o Bibliotecarios (para estos últimos es obligatorio el Código de Empleado).
•   Eliminar Usuario: Permite eliminar usuarios que no posean deudas de libros en la biblioteca.

D. Catálogo Visual (Panel Académico)
•   Visualizador del Catálogo: Dibuja un gráfico de Árbol Binario de Búsqueda (BST). Cada nodo representa un libro, estructurado en base a su código ISBN. Al insertar un libro, se puede observar cómo se crea y posiciona dinámicamente un nodo hijo (izquierdo o derecho) según las propiedades de los árboles de búsqueda binaria.

---

6. ESTRUCTURAS DE DATOS EMPLEADAS EN LA INTERFAZ

El comportamiento visual del sistema responde directamente a estructuras de datos implementadas en el backend:
•   Árbol Binario de Búsqueda (ABB): Estructura en la que se guarda y organiza el Catálogo de Libros, permitiendo búsquedas eficientes por ISBN y mostrándose de manera interactiva en el panel del "Catálogo Visual".
•   Lista Enlazada Doble: Utilizada para el almacenamiento y recorrido lineal de los Usuarios en el sistema, visualizados en la sección de gestión de usuarios.
•   Pila (Stack): Estructura que gestiona el Historial de Operaciones Recientes. Permite deshacer la última acción realizada aplicando la política LIFO (último en entrar, primero en salir).
•   Colas de Espera (Queue): Implementadas de forma FIFO (primero en entrar, primero en salir) por cada libro para gestionar los turnos de espera si el ejemplar se encuentra agotado.

---

7. RESOLUCIÓN DE DUDAS OPERATIVAS COMUNES

•   ¿Qué pasa si un cliente solicita un libro agotado?
    El sistema no rechazará la solicitud, sino que agregará al cliente automáticamente a la cola de espera de ese libro. Cuando otro usuario devuelva el libro, el sistema detectará la cola de espera y asignará el libro al cliente en espera sin que el bibliotecario deba realizar un préstamo manual adicional.

•   ¿Cuántas acciones puedo deshacer?
    Puedes deshacer tantas operaciones como acciones tengas en la pila del historial transaccional de tu sesión actual. El botón "Deshacer" (Undo) irá desapilando los registros cronológicamente, uno por uno, hasta que la pila quede vacía.
