from validaciones import Validaciones
from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError

class Remesa:
    def __init__(self, id_remesa, material, proveedor, cantidad_recibida, saldo_disponible, fecha_recepcion, fecha_vencimiento, precio_unitario):
        self.id_remesa = id_remesa
        self.material = material
        self.proveedor = proveedor

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida

        # Falta validar: saldo_disponible no negativo y no mayor a cantidad_recibida (RN10, RN11)
        self.saldo_disponible = saldo_disponible

        self. fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioInvalidoError("El precio unitario debe ser mayor que cero.")
        self.precio_unitario = precio_unitario
        
    def es_utilizable(self, fecha):
        # Falta validar (RN17)
        return
    
    def vencida(self, fecha):
        # Falta validar (RN17)
        return
    
    def consumir(self, cantidad):
        # Falta validar: cantidad positiva y cantidad <= saldo_disponible (SaldoInvalidoError)
        return

    def movimientos(self):
        return
    
    def validarid():
        return

