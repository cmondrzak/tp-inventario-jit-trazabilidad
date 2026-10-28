class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self._inicio = None

    def esta_vacia(self):
        return self._inicio is None

    def agregar_final(self, dato):
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self._inicio = nuevo
        else:
            actual = self._inicio

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo

    def obtener_datos(self):
        datos = []
        actual = self._inicio

        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        
        return datos

    def eliminar(self, dato):
        actual = self._inicio
        anterior = None

        while actual is not None:
            if actual.dato == dato:
                if anterior is None:
                    self._inicio = actual.siguiente
                else: 
                    anterior.siguiente = actual.siguiente

                return

            anterior = actual
            actual = actual.siguiente

        raise ValueError("El dato no se encuentra en la lista.")
    