class Libro:
    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.estado = "Disponible"

    def esta_disponible(self):
        """Verifica si el libro está disponible para préstamo."""
        return self.estado == "Disponible"

    def marcar_como_prestado(self):
        """Cambia el estado del libro a prestado."""
        self.estado = "Prestado"

    def marcar_como_disponible(self):
        """Cambia el estado del libro a disponible."""
        self.estado = "Disponible"

    def __lt__(self, otro):
        # Permite que cuando se ejecute el arbol de búsqueda binaria, se compare por ISBN y se ordene por este atributo.
        return self.isbn < otro.isbn

    def __str__(self):
        return f"[{self.isbn}] {self.titulo} - {self.autor} ({self.estado})"