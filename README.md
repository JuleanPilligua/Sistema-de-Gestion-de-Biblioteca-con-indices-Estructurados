dentro del archivo logica.py al hacer la importacion solo es 
from modelos import Libro, Cliente, Bibliotecario, Prestamo
from estructuras import ArbolBinarioBusqueda, ListaEnlazadaPersonas, PilaHistorial, ColaEspera

Sistema de Gestión de Biblioteca con Índices Estructurados
1. Descripción del proyecto
El grupo desarrollará un sistema para la gestión de una biblioteca, permitiendo administrar libros, usuarios, préstamos, devoluciones y búsquedas. Sin embargo, a diferencia de un sistema básico administrativo, este proyecto deberá incorporar estructuras de datos específicas para optimizar el acceso y organización de la información.
La idea no es solamente registrar datos, sino demostrar cómo distintas estructuras resuelven problemas concretos dentro del sistema.
2. Objetivo general
Desarrollar un sistema de biblioteca que aplique estructuras de datos adecuadas para organizar, buscar, insertar y recuperar información de manera eficiente.


3. Estructuras de datos que deben aplicarse dentro del proyecto
Este proyecto deberá incorporar obligatoriamente:
•	TAD para representar entidades como Libro, Usuario o Préstamo.
•	Pila para gestionar historial de acciones recientes o deshacer operaciones.
•	Cola para administrar lista de espera de préstamos.
•	Lista enlazada para la gestión de colecciones dinámicas.
•	Árbol binario de búsqueda para indexar libros por código, título o autor.
•	Análisis comparativo básico de complejidad de algunas operaciones.
4. Funcionalidades obligatorias
•	Registrar libros.
•	Registrar usuarios.
•	Registrar préstamos y devoluciones.
•	Buscar libros.
•	Gestionar lista de espera cuando un libro no esté disponible.
•	Mostrar historial reciente de operaciones.
•	Recorrer y mostrar un árbol de búsqueda de libros.
•	Permitir inserción, búsqueda y eliminación sobre la estructura principal seleccionada.

---

## 5. Interfaz Gráfica de Usuario (GUI) con WebView

Se ha implementado una interfaz de usuario moderna basada en **WebView** utilizando `pywebview`. Esta interfaz permite gestionar la biblioteca de forma interactiva y atractiva, conectando directamente con las estructuras de datos desarrolladas en Python.

### Características Principales:
* **Dashboard Completo:** Métricas en tiempo real del estado de la biblioteca (número de libros en el BST, cantidad de usuarios en la lista enlazada, préstamos activos y cantidad de acciones en la pila).
* **Catálogo Visual:** Listado de libros en cuadrícula con tarjetas interactivas e indicadores de disponibilidad a color. Búsqueda instantánea y filtrado por criterios (ISBN, Título, Autor).
* **Gestión de Préstamos y Devoluciones:** Interfaz gráfica para realizar préstamos, encolar clientes en la lista de espera (FIFO) y registrar devoluciones de forma sencilla.
* **Control de Usuarios:** Registro y visualización del listado completo de clientes y bibliotecarios guardados en la Lista Enlazada.
* **Historial Dinámico (Pila):** Historial interactivo que muestra las acciones recientes (apiladas en la Pila) con soporte para la operación de **Deshacer (Undo/Pop)** en orden inverso.
* **Visualizador Interactiva de Estructuras (¡Destacado!):**
  * **Árbol Binario (BST):** Dibuja de manera dinámica el árbol binario de libros con sus conexiones de nodos izquierdo/derecho en un gráfico SVG interactivo.
  * **Lista Enlazada:** Representación lineal de los usuarios mediante nodos enlazados con flechas que apuntan hasta el valor `NULL`.
  * **Pila (Historial):** Renderizado vertical de la pila mostrando el `TOPE` y el flujo de apilamiento LIFO.
  * **Colas de Espera:** Vista de las filas FIFO de clientes esperando por libros específicos.
* **Análisis de Complejidad:** Tabla comparativa interactiva que explica los tiempos de ejecución de las operaciones (O(1), O(log n), O(n)) con medidores gráficos.

### Requisitos de Instalación:

Para ejecutar la interfaz gráfica, es necesario instalar la biblioteca `pywebview`:

```bash
pip install pywebview
```

### Cómo Ejecutar la Interfaz:

Ejecuta el archivo [gui.py](file:///C:/Users/LENOVO/Documents/ULEAM/3%20semestre/Estructura%20de%20datos/Sistema%20de%20Gestion%20de%20Biblioteca/gui.py) desde la terminal:

```bash
python gui.py
```

