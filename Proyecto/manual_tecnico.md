MANUAL TÉCNICO Y DE PROGRAMADOR
Sistema de Gestión de Biblioteca con Índices Estructurados

Este manual está dirigido a desarrolladores, programadores y docentes evaluadores de la arquitectura interna de software del sistema de biblioteca. Describe la organización del código, los modelos orientados a objetos y las especificaciones técnicas de las estructuras de datos personalizadas.

---

1. ARQUITECTURA GENERAL Y DIRECTORIO DE ARCHIVOS

El sistema sigue una arquitectura modular en Python, dividiendo la lógica de negocio, las estructuras de datos, los modelos de entidades, la interfaz de comandos (CLI) y la interfaz gráfica basada en WebView (GUI).

Estructura de archivos del proyecto:
•   main.py: Archivo de entrada principal del sistema en consola. Inicializa las colecciones de prueba y ejecuta el menú CLI.
•   logica.py: Controlador principal (clase GestionBiblioteca). Maneja la coordinación de las transacciones, interactúa con los modelos y conecta las estructuras de datos.
•   acciones.py: Módulo que implementa las acciones reversibles (patrón comando) mediante herencia de clases para dar soporte a la pila de deshacer (Undo).
•   estructuras/: Directorio que contiene las estructuras de datos personalizadas:
    - arbol_binario.py: Implementación del Árbol Binario de Búsqueda (BST) y su nodo correspondiente.
    - lista_enlazada.py: Implementación de la Lista Enlazada Simple y su nodo.
    - pilas_colas.py: Implementación de los TADs Pila y Cola utilizando envoltorios de colecciones optimizadas.
•   modelos/: Directorio que define las clases del dominio bajo principios de Programación Orientada a Objetos:
    - usuario.py: Clase base abstracta de usuario.
    - cliente.py: Clase derivada que representa al cliente de la biblioteca.
    - bibliotecario.py: Clase derivada para los administradores.
    - libro.py: Clase entidad para los libros del catálogo.
    - prestamo.py: Clase entidad para el control de fechas de salida y devolución de libros.
•   gui.py: Puente API que comunica la interfaz gráfica en HTML/JS con los métodos de Python en logica.py.
•   gui.html / gui.css / gui.js: Archivos que conforman la interfaz gráfica interactiva (interfaz web de escritorio renderizada mediante WebView).

---

2. ESPECIFICACIÓN DE MODELOS DE DATOS (POO)

A. Clase Libro (modelos/libro.py)
•   Atributos:
    - isbn (str): Clave de indexación primaria.
    - titulo (str): Título de la obra literaria.
    - autor (str): Autor del libro.
    - estado (str): Estado actual ("Disponible" o "Prestado").
•   Métodos relevantes:
    - __lt__(self, otro): Sobrecarga del operador "menor que" (<) para permitir la comparación automática e inserción ordenada de libros dentro del Árbol Binario de Búsqueda basándose en el ISBN.

B. Jerarquía de Usuarios (modelos/usuario.py, cliente.py, bibliotecario.py)
•   Usuario (Clase Base): Define atributos comunes como idUsuario, nombre, correo y contraseña, y el método verificar_contraseña().
•   Cliente (Derivada): Agrega una lista de prestamosActivos y métodos para agregar préstamos y procesar devoluciones.
•   Bibliotecario (Derivada): Agrega el atributo privado _codigoEmpleado encapsulado con propiedades getter/setter (`@property` / `@codigo_empleado.setter`) para validar que no se guarden códigos vacíos.

C. Clase Prestamo (modelos/prestamo.py)
•   Maneja la lógica transaccional guardando la fecha de salida (fecha de hoy) y calcula la fecha límite automáticamente sumando 14 días. Cuenta con banderas lógicas para registrar o revertir devoluciones.

---

3. DETALLE DE LAS ESTRUCTURAS DE DATOS PERSONALIZADAS (TAD)

A. Árbol Binario de Búsqueda (estructuras/arbol_binario.py)
•   Clase NodoArbol:
    - libro: Instancia del objeto Libro.
    - izquierdo: Referencia al NodoArbol del subárbol izquierdo (ISBN menor).
    - derecho: Referencia al NodoArbol del subárbol derecho (ISBN mayor).
•   Clase ArbolBinarioBusqueda:
    -raiz: Apunta al NodoArbol raíz.
    - insertar(libro): Inserta un libro en el subárbol correspondiente de manera recursiva. Si el ISBN ya existe, evita el duplicado.
    - buscar_por_isbn(isbn): Realiza búsquedas recursivas con complejidad O(log n).
    - eliminar(isbn): Realiza la eliminación física del nodo. En el caso de nodos con dos hijos, localiza recursivamente el sucesor inorden (el nodo con menor valor en su subárbol derecho) para reestructurar las conexiones y mantener la consistencia del árbol.
    - obtener_inorden(): Recorrido inorden recursivo (LNR) que construye una lista secuencial de libros ordenados.

B. Lista Enlazada Simple (estructuras/lista_enlazada.py)
•   Clase NodoLista:
    - persona: Instancia del objeto Usuario (Cliente o Bibliotecario).
    - siguiente: Referencia al siguiente NodoLista.
•   Clase ListaEnlazadaPersonas:
    - cabeza: Apunta al primer NodoLista de la estructura.
    - insertar(persona): Inserta un usuario al final de la lista recorriendo secuencialmente los enlaces hasta encontrar el puntero siguiente nulo.
    - eliminar_por_id(idUsuario): Recorre la lista guardando el nodo anterior. Cuando encuentra el nodo objetivo, reconecta el nodo anterior con el nodo siguiente al eliminado.

C. Pila Historial (estructuras/pilas_colas.py)
•   Clase PilaHistorial:
    - _items: Colección de tipo deque para optimizar accesos rápidos en memoria.
    - apilar(accion): Agrega una acción al tope del historial (operación append).
    - desapilar(): Extrae la acción del tope (operación pop) en tiempo O(1).

D. Cola de Espera (estructuras/pilas_colas.py)
•   Clase ColaEspera:
    - _items: Colección de tipo deque.
    - encolar(cliente): Inserta al cliente al final de la cola (operación append).
    - desencolar(): Extrae al cliente ubicado al frente de la cola (operación popleft) en tiempo O(1).

---

4. MECANISMO DE DESHACER (ACCIONES REVERSIBLES)

El sistema implementa el Patrón Comando a través de la clase base Accion y sus derivadas en el archivo acciones.py:
•   Accion (Clase Base): Define la descripción de la acción y el método abstracto deshacer(biblioteca).
•   AccionRegistroLibro: Al deshacerse, elimina el libro recién registrado del catálogo.
•   AccionRegistroUsuario: Al deshacerse, elimina el usuario de la lista enlazada de personas.
•   AccionPrestamo: Al deshacerse, marca el libro como disponible y remueve el préstamo de la ficha del cliente.
•   AccionColaEspera: Al deshacerse, retira al cliente de la cola de espera de un libro.
•   AccionDevolucion: Es la acción más compleja. Al deshacerse, marca el libro como prestado nuevamente y restaura el préstamo en la ficha del cliente. Si la devolución generó un préstamo automático al siguiente usuario en la cola de espera, este préstamo automático se cancela y dicho cliente es vuelto a encolar al frente de la cola de espera para no perder su turno de prioridad.

Este patrón garantiza que la base de datos mantenga su integridad referencial independientemente de cuántas acciones se deshagan de forma sucesiva.
