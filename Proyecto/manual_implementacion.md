MANUAL DE IMPLEMENTACIÓN
Sistema de Gestión de Biblioteca con Índices Estructurados

Este manual contiene las especificaciones y pasos necesarios para instalar, configurar, ejecutar y realizar el despliegue del sistema de biblioteca en entornos de desarrollo y producción local.

---

1. REQUISITOS PREVIOS DEL SISTEMA

Para garantizar el correcto funcionamiento del sistema, se requiere contar con las siguientes tecnologías instaladas:

A. Entorno de Ejecución
•   Python 3.8 o superior (se recomienda Python 3.10 o 3.11).
•   pip (Administrador de paquetes de Python, incluido por defecto con la instalación oficial de Python).

B. Sistema Operativo y Componentes Gráficos
•   Windows: Funciona de forma nativa. Para la interfaz gráfica (GUI) utiliza el motor webview de Microsoft Edge WebView2.
•   macOS: Requiere los frameworks web nativos de Apple (WebKit).
•   Linux: Requiere instalar bibliotecas del sistema para soporte gráfico antes de compilar dependencias de Python (específicamente GTK 3 y WebKit2GTK).

---

2. INSTALACIÓN DE DEPENDENCIAS

El proyecto utiliza la biblioteca pywebview para crear una ventana de escritorio nativa que renderiza la interfaz HTML/JS/CSS de forma local.

Pasos para la instalación en Windows:
1. Abra una terminal de comandos (cmd o PowerShell) en el directorio raíz del proyecto.
2. Ejecute el siguiente comando para instalar pywebview:
   pip install pywebview

Pasos para la instalación en Linux (Debian/Ubuntu):
Antes de instalar pywebview mediante pip, es necesario instalar las dependencias de sistema mediante apt:
1. Ejecute en su terminal:
   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
2. Luego instale el paquete de Python:
   pip install pywebview

---

3. INSTRUCCIONES DE EJECUCIÓN (INICIO DEL SISTEMA)

El sistema soporta dos modos de funcionamiento independientes.

A. Ejecución en Modo Consola (CLI)
Este modo es ideal para pruebas rápidas y depuración directa, no requiere dependencias gráficas avanzadas.
1. Abra la terminal en la raíz del proyecto.
2. Ejecute el comando:
   python main.py

B. Ejecución en Modo Interfaz Gráfica (GUI)
Este modo arranca una aplicación interactiva que permite ver de forma gráfica las estructuras de datos.
1. Abra la terminal en la raíz del proyecto.
2. Ejecute el comando:
   python gui.py

---

4. CONFIGURACIÓN DE DATOS SEMILLA (INICIALIZACIÓN)

El sistema está configurado para inicializarse con una base de datos en memoria para propósitos puramente académicos. Cada vez que la aplicación se inicia, se ejecuta la función inicializar_datos() (definida en main.py y reutilizada en gui.py). 

Esta función realiza las siguientes tareas de manera automática:
•   Registra el usuario administrador por defecto (id: L01, email: admin@biblioteca.com).
•   Registra tres usuarios cliente para pruebas (Juan Pérez, María López, Carlos Mendoza).
•   Registra cuatro libros con sus respectivos ISBN (códigos 9781 al 9784).
•   Limpia la pila de historial transaccional para que el usuario empiece con su historial vacío y listo para probar la opción de "Deshacer".

Si desea agregar o modificar los datos semilla por defecto, puede editar directamente el archivo main.py en su función inicializar_datos() utilizando un editor de texto.

---

5. RESOLUCIÓN DE PROBLEMAS COMUNES (TROUBLESHOOTING)

•   Problema: Error al ejecutar gui.py debido a "ModuleNotFoundError: No module named 'webview'".
    Solución: La dependencia pywebview no está instalada en el entorno actual de Python. Ejecute 'pip install pywebview' en su terminal. Si utiliza un entorno virtual (venv), asegúrese de tener activado dicho entorno antes de instalar.

•   Problema: La ventana de la interfaz gráfica se abre pero se queda en blanco o no carga los estilos.
    Solución en Windows: Asegúrese de tener instalado Microsoft Edge WebView2 Runtime en su sistema operativo. En sistemas Windows 10 y 11 modernos esto ya viene instalado de fábrica; en versiones anteriores se puede descargar gratis desde el sitio oficial de Microsoft.

•   Problema: La terminal muestra errores de codificación de caracteres en Windows al ejecutar main.py en consola.
    Solución: Python usa por defecto la codificación del sistema. Si los caracteres especiales (como las viñetas "•") se ven corruptos, configure su terminal PowerShell o CMD a codificación UTF-8 ejecutando el comando:
    chcp 65001
    antes de correr 'python main.py'.
