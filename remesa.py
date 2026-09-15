from validaciones import Validaciones


class Remesa:
    def __init__(self, id_remesa, material, proveedor, cantidad_recibida, saldo_disponible, fecha_recepcion, fecha_vencimiento, precio_unitario):
        self.id_remesa = id_remesa
        self.material = material
        self.proveedor = proveedor

        if not Validaciones.es_positivo(cantidad_recibida):
            raise ValueError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida

        self.saldo_disponible = saldo_disponible
        self. fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento

        if not Validaciones.es_positivo(precio_unitario):
            raise ValueError("El precio unitario debe ser mayor que cero.")
        self.precio_unitario = precio_unitario
        
    def es_utilizable(self):
        return
    
    def vencida(self):
        return
    
    def movimientos(self):
        return
    def validarid():
        return
