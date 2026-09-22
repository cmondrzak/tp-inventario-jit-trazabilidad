from exceptions import CantidadInvalidaError, SaldoInvalidoError
from validaciones import Validaciones

class Remesa:
    lista_id=[]
    def __init__(self, id_remesa, material, proveedor, renglon_pedido, cantidad_recibida, saldo_disponible, **datos_opcionales):
        self.id_remesa = id_remesa
        self.material = material
        self.renglon_pedido = renglon_pedido
        self.proveedor = proveedor

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida
        self.saldo_disponible = cantidad_recibida

        self.datos_opcionales = dict(datos_opcionales)
        
    # --- datos opcionales (kwargs) ---------------------------------------

    def obtener_dato(self, clave, default=None):
        """Acceso genérico a cualquier dato opcional guardado por clave."""
        return self.datos_opcionales.get(clave, default)

    def obtener_fecha_vencimiento(self):
        return self.datos_opcionales.get("fecha_vencimiento")

    # --- getters -----------------------------------------------------------

    def obtener_material(self):
        return self.material.get("material")

    def obtener_cantidad_recibida(self):
        return self.cantidad_recibida.get("cantidad_recibida")
    
    # --- estado / consumo --------------------------------------------------

    def esta_vencida(self, fecha):
        """RN17: sin fecha de vencimiento, la remesa nunca está vencida."""
        if self.fecha_vencimiento is None:
            return False
        return self.fecha_vencimiento < fecha

    def es_utilizable(self, fecha):
        """RN17: saldo disponible > 0 y no vencida en `fecha`."""
        return self.saldo_disponible > 0 and not self.esta_vencida(fecha)

    def consumir(self, cantidad):
        """
        Único método que puede reducir el saldo. RN10/RN11 quedan
        garantizadas acá adentro: nunca se puede pedir más de lo que
        hay disponible ni una cantidad no positiva.
        """
        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError("La cantidad a consumir debe ser mayor que cero.")
        if cantidad > self.saldo_disponible:
            raise SaldoInvalidoError(
                f"Saldo insuficiente en remesa {self.id_remesa!r}: "
                f"disponible {self.saldo_disponible}, solicitado {cantidad}."
            )
        self.saldo_disponible -= cantidad

    def registrar_retiro(self, id_movimiento_retiro):
        """RN25/RN26: guarda la trazabilidad remesa -> retiros."""
        self.retiros_ids.append(id_movimiento_retiro)

    def __repr__(self):
        return (f"Remesa({self.id_remesa!r}, saldo={self.saldo_disponible}/"
                f"{self.cantidad_recibida}, vto={self.fecha_vencimiento})")
    
    def generar_movimiento_ingreso():
        return
    