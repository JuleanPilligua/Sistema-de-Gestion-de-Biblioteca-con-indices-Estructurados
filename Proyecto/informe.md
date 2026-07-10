INFORME DE ESTRUCTURAS DE DATOS Y EFICIENCIA ALGORÍTMICA
Sistema de Gestión de Biblioteca con Índices Estructurados

Este informe contiene el sustento conceptual obligatorio sobre las estructuras de datos implementadas en el proyecto, justificando su elección, describiendo las operaciones que resuelven, sus ventajas y un análisis comparativo de su complejidad algorítmica (eficiencia).


1. Sustento Conceptual de las Estructuras Utilizadas

A. Árbol Binario de Búsqueda (TAD ArbolBinarioBusqueda)
•   Qué operación resuelve: Indexación y búsqueda de libros en el catálogo mediante su código único (ISBN). También provee un recorrido inorden para mostrar el catálogo ordenado de forma alfabética/numérica.
•   Por qué se eligió: Al buscar un libro en una colección grande, recorrer uno a uno todos los elementos (búsqueda secuencial) es ineficiente. Un Árbol Binario de Búsqueda (BST) permite tomar decisiones de bifurcación izquierda o derecha, descartando la mitad de las opciones en cada paso de manera similar a una búsqueda binaria.
•   Ventajas:
    - Búsquedas, inserciones y eliminaciones promedio en tiempo logarítmico O(log n).
    - Mantiene los datos ordenados de forma natural sin necesidad de algoritmos de ordenamiento costosos adicionales (se obtiene mediante recorrido Inorden).

B. Lista Enlazada Simple (TAD ListaEnlazadaPersonas)
•   Qué operación resuelve: Registro y almacenamiento dinámico de usuarios (Clientes y Bibliotecarios) en el sistema.
•   Por qué se eligió: El número de usuarios registrados en una biblioteca es indeterminado y cambia constantemente. Una lista enlazada permite asignar memoria de forma dinámica a medida que se registran nuevos usuarios, evitando el costo de redimensionamiento contiguo que sufren los arreglos estándar.
•   Ventajas:
    - Inserción en tiempo constante O(1) al inicio de la lista.
    - No requiere bloques de memoria contiguos, lo que previene la fragmentación y optimiza el uso de memoria en sistemas dinámicos.

C. Pila (TAD PilaHistorial)
•   Qué operación resuelve: Gestión del historial de operaciones realizadas por cada usuario y soporte para la funcionalidad de revertir/deshacer la última acción (Undo).
•   Por qué se eligió: Se requiere un comportamiento LIFO (Last In, First Out - Último en entrar, Primero en salir). Para poder deshacer una operación, la última acción ejecutada debe ser la primera en revertirse.
•   Ventajas:
    - Control estricto del orden cronológico inverso de las operaciones.
    - Operaciones de apilar (push) y desapilar (pop) extremadamente rápidas en tiempo constante O(1).

D. Cola (TAD ColaEspera)
•   Qué operación resuelve: Administración de la lista de espera de clientes interesados en libros que ya se encuentran prestados.
•   Por qué se eligió: Se requiere un comportamiento FIFO (First In, First Out - Primero en entrar, Primero en salir). El primer cliente en solicitar el libro no disponible debe tener la máxima prioridad para recibirlo cuando este sea devuelto.
•   Ventajas:
    - Garantiza equidad y orden de llegada estricto para los usuarios.
    - Inserción al final (enqueue) y extracción al inicio (dequeue) en tiempo constante O(1).


2. Requisitos de Complejidad Algorítmica (Notación Big-O)

A continuación se detalla la complejidad temporal de las operaciones implementadas en cada estructura de datos del sistema:

Estructura: Árbol Binario de Búsqueda (ISBN)
•   Búsqueda: Caso Promedio O(log n) | Peor Caso O(n)
    Justificación: El peor caso ocurre si el árbol se desbalancea completamente convirtiéndose en una lista.
•   Inserción: Caso Promedio O(log n) | Peor Caso O(n)
    Justificación: Requiere buscar el lugar adecuado antes de insertar el nodo hoja.
•   Eliminación: Caso Promedio O(log n) | Peor Caso O(n)
    Justificación: Requiere buscar el nodo y, de tener 2 hijos, hallar su sucesor inorden.
•   Recorrido Inorden: Caso Promedio O(n) | Peor Caso O(n)
    Justificación: Se deben visitar todos los n nodos exactamente una vez para listarlos.

Estructura: Lista Enlazada Simple
•   Inserción (al final): Caso Promedio O(n) | Peor Caso O(n)
    Justificación: Se recorre desde la cabeza hasta el último nodo actual para enlazar el nuevo.
•   Búsqueda (por ID/Correo): Caso Promedio O(n) | Peor Caso O(n)
    Justificación: Búsqueda secuencial lineal; en el peor caso el elemento está al final o no existe.
•   Eliminación (por ID): Caso Promedio O(n) | Peor Caso O(n)
    Justificación: Requiere buscar secuencialmente el nodo antes de reconectar los enlaces.

Estructura: Pila (Historial)
•   Apilar (push): Caso Promedio O(1) | Peor Caso O(1)
    Justificación: Operación directa sobre el tope de la estructura.
•   Desapilar (pop): Caso Promedio O(1) | Peor Caso O(1)
    Justificación: Extracción directa del elemento en el tope de la estructura.

Estructura: Cola (Espera)
•   Encolar (enqueue): Caso Promedio O(1) | Peor Caso O(1)
    Justificación: Inserción directa al final de la cola.
•   Desencolar (dequeue): Caso Promedio O(1) | Peor Caso O(1)
    Justificación: Remoción directa desde el frente de la cola.


3. Comparación Básica de Eficiencia

Para demostrar el impacto real de las estructuras de datos, se comparan dos soluciones alternativas para la búsqueda de un libro en un catálogo de n elementos:

Solución A: Búsqueda Secuencial (Lista Enlazada o Lista Simple)
•   Si los libros se almacenan en una lista enlazada o un arreglo desordenado, buscar un libro por su ISBN requiere comparar el valor con cada elemento uno por uno, comenzando por el primero.
•   Complejidad Temporal: O(n).
•   Ejemplo práctico: Si la biblioteca tiene 1,000,000 de libros y buscamos uno que no existe o está al final, realizaremos 1,000,000 de comparaciones.

Solución B: Búsqueda Binaria (Árbol Binario de Búsqueda - BST)
•   Dado que el catálogo está organizado como un árbol binario de búsqueda indexado por ISBN, cada comparación nos permite ir al subárbol izquierdo (si el ISBN buscado es menor) o al derecho (si es mayor).
•   Complejidad Temporal: O(log n) en promedio.
•   Ejemplo práctico: Para el mismo catálogo de 1,000,000 de libros, el número máximo de comparaciones en el caso promedio está acotado por aproximadamente 20 comparaciones.

Conclusión del análisis de eficiencia:
La diferencia de rendimiento entre O(n) y O(log n) es masiva a medida que la biblioteca crece. Mientras que la Solución A requiere un tiempo lineal que escala proporcionalmente con el número de libros, la Solución B mantiene un tiempo de respuesta casi instantáneo (escala logarítmicamente), lo cual justifica plenamente el uso del Árbol Binario de Búsqueda como la estructura principal para el catálogo.
