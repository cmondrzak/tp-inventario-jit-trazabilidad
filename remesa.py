from validaciones import Validaciones
from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError

class Remesa:
    lista_id=[]
    def __init__(self, id_remesa, material,renglon_pedido ,cantidad_recibida, fecha_vencimiento):
        self.id_remesa = id_remesa
        self.material = material
        self.renglon_pedido=renglon_pedido

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida

        self.fecha_vencimiento = fecha_vencimiento

    def esta_vencida():
        return
    
    def generar_movimiento_ingreso():
        return
    