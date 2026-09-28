from exceptions import CantidadInvalidaError, FechaInvalidaError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError
from validaciones import Validaciones
from datetime import date

class Remesa:
    lista_id=[]
    def __init__(self, id_remesa, material, proveedor, renglon_pedido, cantidad_recibida, fecha_recepcion = None, **datos_opcionales):
        if not Validaciones.validarid(Remesa.lista_id, id_remesa):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if material is None:
            raise MaterialNoEncontradoError("El material no puede estar vacío.")
        
        if proveedor is None:
            raise ProveedorNoEncontradoError("El Proveedor no puede estar vacío.")

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")

        if fecha_recepcion is None:
            fecha_recepcion = date.today()

        if not Validaciones.es_fecha(fecha_recepcion):
            raise FechaInvalidaError("La fecha de recepción no es válida.")

        fecha_vencimiento = datos_opcionales.get("fecha_vencimiento")
        if fecha_vencimiento is not None and not Validaciones.es_fecha(fecha_vencimiento):
            raise FechaInvalidaError("La fecha de vencimiento no es válida.")

        self.id_remesa = id_remesa
        self.material = material
        self.proveedor = proveedor
        self.cantidad_recibida = cantidad_recibida
        self.saldo_disponible = cantidad_recibida
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        self.datos_opcionales = dict(datos_opcionales)
        Remesa.lista_id.append(self.id_remesa)

        self.renglon_pedido = renglon_pedido

    def obtener_dato(self, clave, default=None):
        return self.datos_opcionales.get(clave, default)

    def obtener_fecha_vencimiento(self):
        return self.fecha_vencimiento

    def obtener_material(self):
        return self.material

    def obtener_cantidad_recibida(self):
        return self.cantidad_recibida
    
    def esta_vencida(self, fecha):
        if self.fecha_vencimiento is None:
            return False
        return self.fecha_vencimiento < fecha

    def es_utilizable(self, fecha):
        return self.saldo_disponible > 0 and not self.esta_vencida(fecha)

    def consumir(self, cantidad):
        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError("La cantidad a consumir debe ser mayor que cero.")
        if cantidad > self.saldo_disponible:
            raise SaldoInvalidoError(
                f"Saldo insuficiente en remesa {self.id_remesa!r}: "
                f"disponible {self.saldo_disponible}, solicitado {cantidad}."
            )
        self.saldo_disponible -= cantidad
        
    def __repr__(self):
        return (f"Remesa({self.id_remesa!r}, saldo={self.saldo_disponible}/"
                f"{self.cantidad_recibida}, vto={self.fecha_vencimiento})")
    
    def generar_movimiento_ingreso():
        return
    
    def obtener_idremesa(self):
        return self.id_remesa

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []