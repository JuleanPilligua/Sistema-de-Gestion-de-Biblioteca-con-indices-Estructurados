class Libro:
    def __init__(self, isbn, titulo, autor, categoria, estado, vecesPrestado, colaEspera):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.estado = estado
        self.vecesPrestado = vecesPrestado
        self.colaEspera = cola() #Esta funcion estará en una carpeta llamada estructuras, al mismo nivel que "modelos", dentro de la carpeta "estructuras", existiran archivos como pila.py, cola.py, etc, que nos permitiran crear un objeto el cual se utilizará para cada libro en este caso de cola()

    def prestar():
        pass

    def devolver():
        pass

    def mostrarInfo():
        pass