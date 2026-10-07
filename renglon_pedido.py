from validaciones import Validaciones
from exceptions import CantidadInvalidaError, MaterialInvalidoError, PrecioInvalidoError, SaldoInvalidoError, IdentificadorDuplicadoError

class Renglon_pedido:
    lista_id=[]
    def __init__(self,id_renglon ,material, cantidad, precio_unitario):
        if not Validaciones.validarid(Renglon_pedido.lista_id,id_renglon):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(material):
            raise MaterialInvalidoError("El material no puede estar vacío.")
        
        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero.")

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioInvalidoError("El precio unitario debe ser mayor que cero.")

        self.id_renglon=id_renglon
        self.material = material
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        Renglon_pedido.lista_id.append(self.id_renglon)

    def subtotal_renglon(self):
        return self.cantidad * self.precio_unitario
    
    def obtener_id_renglon_pedido(self):
        return self.id_renglon
