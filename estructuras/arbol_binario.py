class NodoArbol:
    def __init__(self, libro):
        self.libro = libro
        self.izquierdo = None
        self.derecho = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        if self.raiz is None:
            self.raiz = NodoArbol(libro)
        else:
            self._insertar_recursivo(self.raiz, libro)

    def _insertar_recursivo(self, nodo, libro):
        if libro.isbn < nodo.libro.isbn:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(libro)
            else:
                self._insertar_recursivo(nodo.izquierdo, libro)
        elif libro.isbn > nodo.libro.isbn:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(libro)
            else:
                self._insertar_recursivo(nodo.derecho, libro)
        else:
            # Si el ISBN ya existe, no se inserta duplicado
            pass

    def buscar_por_isbn(self, isbn):
        return self._buscar_por_isbn_recursivo(self.raiz, isbn)

    def _buscar_por_isbn_recursivo(self, nodo, isbn):
        if nodo is None:
            return None
        if isbn == nodo.libro.isbn:
            return nodo.libro
        elif isbn < nodo.libro.isbn:
            return self._buscar_por_isbn_recursivo(nodo.izquierdo, isbn)
        else:
            return self._buscar_por_isbn_recursivo(nodo.derecho, isbn)

    def buscar_por_titulo(self, titulo):
        # Búsqueda secuencial (complejidad O(N)) en el árbol inorden
        resultados = []
        self._buscar_por_titulo_recursivo(self.raiz, titulo.lower(), resultados)
        return resultados

    def _buscar_por_titulo_recursivo(self, nodo, titulo, resultados):
        if nodo:
            self._buscar_por_titulo_recursivo(nodo.izquierdo, titulo, resultados)
            if titulo in nodo.libro.titulo.lower():
                resultados.append(nodo.libro)
            self._buscar_por_titulo_recursivo(nodo.derecho, titulo, resultados)

    def buscar_por_autor(self, autor):
        # Búsqueda secuencial (complejidad O(N)) en el árbol inorden
        resultados = []
        self._buscar_por_autor_recursivo(self.raiz, autor.lower(), resultados)
        return resultados

    def _buscar_por_autor_recursivo(self, nodo, autor, resultados):
        if nodo:
            self._buscar_por_autor_recursivo(nodo.izquierdo, autor, resultados)
            if autor in nodo.libro.autor.lower():
                resultados.append(nodo.libro)
            self._buscar_por_autor_recursivo(nodo.derecho, autor, resultados)

    def eliminar(self, isbn):
        self.raiz, eliminado = self._eliminar_recursivo(self.raiz, isbn)
        return eliminado

    def _eliminar_recursivo(self, nodo, isbn):
        if nodo is None:
            return None, None
        
        eliminado = None
        if isbn < nodo.libro.isbn:
            nodo.izquierdo, eliminado = self._eliminar_recursivo(nodo.izquierdo, isbn)
        elif isbn > nodo.libro.isbn:
            nodo.derecho, eliminado = self._eliminar_recursivo(nodo.derecho, isbn)
        else:
            # Nodo encontrado
            eliminado = nodo.libro
            if nodo.izquierdo is None:
                return nodo.derecho, eliminado
            elif nodo.derecho is None:
                return nodo.izquierdo, eliminado
            else:
                # Nodo con dos hijos: obtener sucesor inorden (mínimo en subárbol derecho)
                sucesor = self._obtener_minimo(nodo.derecho)
                nodo.libro = sucesor.libro
                nodo.derecho, _ = self._eliminar_recursivo(nodo.derecho, sucesor.libro.isbn)
                
        return nodo, eliminado

    def _obtener_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def obtener_inorden(self):
        libros = []
        self._inorden_recursivo(self.raiz, libros)
        return libros

    def _inorden_recursivo(self, nodo, libros):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, libros)
            libros.append(nodo.libro)
            self._inorden_recursivo(nodo.derecho, libros)