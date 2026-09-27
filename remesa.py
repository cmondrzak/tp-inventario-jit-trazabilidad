from exceptions import CantidadInvalidaError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError
from validaciones import Validaciones

class Remesa:
    lista_id=[]
    def __init__(self, id_remesa, material, proveedor, renglon_pedido, cantidad_recibida, saldo_disponible, **datos_opcionales):
        if not Validaciones.validarid(Remesa.lista_id, id_remesa):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(material):
            raise MaterialNoEncontradoError("El Material no puede estar vacio.")

        if not Validaciones.es_no_vacio(proveedor):
            raise ProveedorNoEncontradoError("El Proveedor no puede estar vacio.")

        self.id_remesa = id_remesa
        self.material = material
        self.renglon_pedido = renglon_pedido
        self.proveedor = proveedor

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida
        self.saldo_disponible = cantidad_recibida

        self.datos_opcionales = dict(datos_opcionales)
        
    def obtener_dato(self, clave, default=None):
        return self.datos_opcionales.get(clave, default)

    def obtener_fecha_vencimiento(self):
        return self.datos_opcionales.get("fecha_vencimiento")

    def obtener_material(self):
        return self.material.get("material")

    def obtener_cantidad_recibida(self):
        return self.cantidad_recibida.get("cantidad_recibida")
    
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