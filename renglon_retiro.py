from validaciones import Validaciones
from exceptions import CantidadInvalidaError, MaterialNoEncontradoError, PrecioInvalidoError, SaldoInvalidoError, RemesaNoEncontradaError

class RenglonRetiro:
    def __init__(self, id_material, cantidad_solicitada):

        if not Validaciones.es_no_vacio(id_material):
            raise MaterialNoEncontradoError("El material no puede estar vacío.")
        
        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadInvalidaError("La cantidad solicitada debe ser mayor que cero.")

        self.id_material = id_material 
        self.cantidad_solicitada = cantidad_solicitada
    