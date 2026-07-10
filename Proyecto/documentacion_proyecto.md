# DOCUMENTACIÓN DEL PROYECTO: SISTEMA DE GESTIÓN DE BIBLIOTECA
## Aplicación Práctica de Estructuras de Datos y Complejidad Algorítmica

---

### 1. INTRODUCCIÓN

En la actualidad, la administración de la información en las instituciones exige sistemas de software que no solo registren datos de forma pasiva, sino que garanticen un acceso rápido, consistente y eficiente. Los sistemas de gestión de bases de datos tradicionales suelen almacenar y buscar la información de forma lineal, lo cual resulta altamente ineficiente a medida que el volumen de los registros crece exponencialmente.

Este proyecto presenta el desarrollo del **Sistema de Gestión de Biblioteca con Índices Estructurados**. Diseñado bajo principios de ingeniería de software y teoría de estructuras de datos, el sistema implementa Tipos Abstractos de Datos (TADs) personalizados para optimizar la organización y consulta de libros, la administración de usuarios, la asignación de turnos de reserva y la gestión de transacciones. 

Mediante el modelado de clases de Python y el uso de punteros y referencias de memoria reales, el proyecto demuestra cómo el diseño algorítmico apropiado optimiza los recursos computacionales y resuelve problemas operativos comunes como cuellos de botella en búsquedas a gran escala, tiempos de espera equitativos y consistencia transaccional.

---

### 2. OBJETIVOS

#### Objetivo General
Desarrollar e implementar un Sistema de Gestión de Biblioteca estructurado en Python que aplique estructuras de datos lineales y jerárquicas dinámicas para organizar, buscar, insertar y recuperar información con la máxima eficiencia temporal y espacial.

#### Objetivos Específicos
* Modelar el catálogo de libros mediante un **Árbol Binario de Búsqueda (BST)** indexado por ISBN para lograr búsquedas, inserciones y eliminaciones en tiempo promedio logarítmico O(log n).
* Implementar una **Lista Enlazada Simple** personalizada para la administración dinámica de los usuarios (Clientes y Bibliotecarios), evitando el uso de arrays contiguos predefinidos y optimizando el consumo de memoria.
* Utilizar una **Pila** para almacenar cronológicamente el historial transaccional de los usuarios y posibilitar la reversión total de la última operación (*Undo*).
* Utilizar una **Cola** para gestionar de forma equitativa las colas de espera de aquellos libros que se encuentran prestados, siguiendo el principio FIFO (*First In, First Out*).
* Proveer una **Interfaz Gráfica de Usuario (GUI)** dinámica e interactiva que grafique visualmente el estado físico de los nodos y referencias de las estructuras en tiempo real.

---

### 3. DESCRIPCIÓN DEL PROBLEMA

El flujo de trabajo habitual de una biblioteca implica operaciones continuas de inserción (registrar nuevos libros y usuarios), búsquedas exhaustivas (localizar obras por ISBN, título o autor) y actualizaciones transaccionales (préstamos y devoluciones). 

Cuando estos sistemas se desarrollan utilizando de forma exclusiva estructuras integradas en lenguajes de alto nivel (como las listas nativas de Python que actúan como arrays dinámicos contiguos), se incurre en graves problemas de rendimiento a gran escala:
1. **Búsquedas Ineficientes:** Localizar un libro en un catálogo de miles de elementos obliga al procesador a realizar búsquedas secuenciales de coste lineal O(n). A medida que el número de libros crece, el sistema se vuelve lento.
2. **Desperdicio o Reasignación de Memoria:** Almacenar usuarios en arrays contiguos requiere reasignaciones y copia de elementos en memoria cada vez que el tamaño del contenedor se excede.
3. **Falta de Equidad en Reservas:** Cuando múltiples usuarios solicitan un mismo libro prestado, la ausencia de un sistema ordenado de turnos genera inconsistencia y disputas por prioridad.
4. **Ausencia de Reversibilidad:** En entornos reales, los bibliotecarios cometen errores de captura y registro. Sin un historial estructurado de transacciones, deshacer una acción errónea (como una devolución mal registrada) puede corromper el estado general de la base de datos.

Por lo tanto, se hace indispensable construir un sistema que resuelva estos problemas aplicando de forma nativa la teoría de estructuras de datos.

---

### 4. ESTRUCTURAS IMPLEMENTADAS Y JUSTIFICACIÓN

El sistema basa todo su funcionamiento en cuatro estructuras de datos personalizadas, justificadas bajo criterios de eficiencia técnica:

#### A. Árbol Binario de Búsqueda (TAD ArbolBinarioBusqueda)
* **Justificación de uso:** Las búsquedas en el catálogo de libros son las operaciones más repetitivas del sistema. Al estructurar el catálogo jerárquicamente por medio de un BST indexado por el ISBN, cada comparación permite descartar la mitad del árbol restante. Esto reduce drásticamente el número de operaciones necesarias en comparación con una búsqueda lineal.
* **Operación que resuelve:** Búsqueda rápida de libros por código ISBN, inserción ordenada y eliminación de libros del catálogo, además del recorrido ordenado de elementos.

#### B. Lista Enlazada Simple (TAD ListaEnlazadaPersonas)
* **Justificación de uso:** El número de clientes y bibliotecarios es indeterminado y dinámico. La lista enlazada permite la inserción de nuevos elementos de forma descentralizada en memoria física, enlazando nodos a través de punteros de referencia (`NodoLista`). Esto elimina la necesidad de memoria contigua.
* **Operación que resuelve:** Registro de nuevos usuarios y persistencia temporal del listado general de personas autorizadas en el sistema.

#### C. Pila (TAD PilaHistorial)
* **Justificación de uso:** Para implementar la funcionalidad de deshacer operaciones (*Undo*), es necesario guardar el estado anterior en el orden inverso al que ocurrieron los hechos. La estructura de Pila cumple con esta necesidad LIFO (último en entrar, primero en salir), asegurando que la última operación ejecutada sea la primera en ser extraída y revertida.
* **Operación que resuelve:** Almacenar de forma ordenada los objetos de tipo `Accion` generados por el usuario para posibilitar la reversión de transacciones.

#### D. Cola (TAD ColaEspera)
* **Justificación de uso:** Garantiza el trato equitativo e imparcial a los clientes. Al estructurar las reservas en una Cola (FIFO), se asegura que el cliente que esperó durante más tiempo sea el primero al que se le asigne automáticamente el libro cuando este sea devuelto a la biblioteca.
* **Operación que resuelve:** Organización de prioridades y turnos en libros no disponibles.

---

### 5. OPERACIONES DESARROLLADAS EN CADA ESTRUCTURA

#### En el Árbol Binario de Búsqueda
* `insertar(libro)`: Compara recursivamente el ISBN del nuevo libro con los nodos existentes (izquierda si es menor, derecha si es mayor) hasta encontrar una hoja vacía para crear el nuevo `NodoArbol`.
* `buscar_por_isbn(isbn)`: Realiza una búsqueda recursiva descendente de tipo binario.
* `eliminar(isbn)`: Localiza el nodo y lo remueve controlando los tres casos de eliminación de un BST (nodo sin hijos, nodo con un único hijo y nodo con dos hijos mediante la búsqueda del sucesor inorden).
* `obtener_inorden()`: Ejecuta un recorrido inorden (Izquierdo - Raíz - Derecho) para obtener una lista ordenada secuencial de todos los libros registrados.

#### En la Lista Enlazada
* `insertar(persona)`: Instancia un `NodoLista` y recorre la estructura hasta encontrar el nodo final (`actual.siguiente == None`) para enlazar el nuevo nodo.
* `buscar_por_id(idUsuario)` / `buscar_por_correo(correo)`: Recorren secuencialmente los nodos desde la cabeza de la lista comparando el valor clave.
* `eliminar_por_id(idUsuario)`: Localiza el usuario objetivo y enlaza el nodo anterior directamente con el nodo siguiente al eliminado, liberando la referencia de memoria.

#### En la Pila
* `apilar(accion)`: Inserta un objeto de acción transaccional en el tope de la estructura.
* `desapilar()`: Retorna y extrae el objeto situado en el tope de la pila para su ejecución inversa.

#### En la Cola
* `encolar(cliente)`: Inserta un cliente al final de la estructura de turnos del libro.
* `desencolar()`: Extrae y retorna el cliente ubicado al frente de la cola de espera para asignarle el libro disponible de inmediato.

---

### 6. ANÁLISIS BÁSICO DE COMPLEJIDAD (NOTACIÓN BIG-O)

| Estructura / TAD | Operación Principal | Complejidad Caso Promedio | Complejidad Peor Caso | Justificación Técnica |
| :--- | :--- | :---: | :---: | :--- |
| **Árbol Binario de Búsqueda** | Búsqueda por ISBN | O(log n) | O(n) | El caso promedio es logarítmico. El peor caso ocurre si los ISBN se ingresan de forma ordenada, degenerando el árbol en una lista lineal. |
| | Inserción | O(log n) | O(n) | Requiere recorrer el árbol binariamente hasta hallar la posición de inserción adecuada. |
| | Eliminación | O(log n) | O(n) | Requiere localizar el nodo y reorganizar sus subárboles. |
| | Recorrido Inorden | O(n) | O(n) | Es necesario recorrer obligatoriamente cada uno de los $n$ nodos para poder listarlos ordenadamente. |
| **Lista Enlazada Simple** | Inserción | O(n) | O(n) | En la implementación actual, se debe recorrer desde la cabeza hasta el último nodo para agregar el nuevo. |
| | Búsqueda por ID | O(n) | O(n) | Requiere una búsqueda secuencial lineal de principio a fin de la lista. |
| | Eliminación por ID | O(n) | O(n) | Requiere una búsqueda lineal para encontrar el nodo a borrar y actualizar sus punteros. |
| **Pila** | Apilar (*push*) | O(1) | O(1) | El acceso y la inserción se realizan de manera directa sobre el tope del historial. |
| | Desapilar (*pop*) | O(1) | O(1) | La extracción se hace de forma directa del elemento más reciente en el tope. |
| **Cola** | Encolar (*enqueue*) | O(1) | O(1) | Se añade al final de la cola en tiempo constante utilizando referencias rápidas. |
| | Desencolar (*dequeue*) | O(1) | O(1) | Se extrae directamente el nodo situado al inicio de la cola. |

---

### 7. MEJORAS E INNOVACIONES IMPLEMENTADAS

* **Patrón de Reversión Completa (Deshacer Transacciones)**: A través de objetos encapsulados de acciones (`AccionRegistroLibro`, `AccionPrestamo`, `AccionDevolucion`, etc.), el sistema no solo registra que algo pasó, sino que guarda los datos necesarios para revertir el estado del sistema. Si se comete un error, el sistema desapila la acción de la Pila de historial y realiza el proceso inverso de forma matemática e íntegra.
* **Procesamiento de Préstamos Automatizado por Cola**: Al registrar la devolución de un libro prestado, la lógica del sistema detecta si existe una cola de espera para dicho ISBN. Si es así, de forma completamente automatizada, desencola al primer cliente en espera, genera su nuevo préstamo y le asigna el libro sin requerir intervención manual externa.
* **Interfaz de Visualización de Estructuras (GUI Interactiva)**: Se desarrolló una interfaz gráfica moderna utilizando PyWebView con HTML5, JS (con renderizado dinámico en Canvas/DOM) y CSS3. La interfaz cuenta con una sección dedicada de visualización que dibuja gráficamente el árbol de búsqueda, la lista enlazada, la pila de historial y las colas de espera en tiempo real, facilitando la comprensión académica de cómo cambian los nodos y enlaces en memoria con cada acción realizada.
