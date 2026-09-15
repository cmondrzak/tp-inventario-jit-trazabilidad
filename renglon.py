from validaciones import Validaciones
from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError

class Renglon:
    def __init__(self, material, cantidad, precio_unitario):
        self.material = material

        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero.")
        self.cantidad = cantidad

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioInvalidoError("El precio unitario debe ser mayor que cero.")
        self.precio_unitario = precio_unitario
        
    def subtotal_renglon(self):
        return self.cantidad * self.precio_unitario
    def validarid():
        return

