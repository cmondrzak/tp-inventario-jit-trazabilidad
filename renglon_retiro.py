from validaciones import Validaciones
from exceptions import CantidadInvalidaError, MaterialNoEncontradoError, PrecioInvalidoError, SaldoInvalidoError, RemesaNoEncontradaError

class RenglonRetiro:
    def __init__(self, material, remesa_modificada, cantidad_solicitada):

        if not Validaciones.es_no_vacio(material):
            raise MaterialNoEncontradoError("El material no puede estar vacío.")
        
        if remesa_modificada is None:
            raise RemesaNoEncontradaError("Tiene que haber una remesa modificada")
        
        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadInvalidaError("La cantidad solicitada debe ser mayor que cero.")

        self.material = material
        self.remesa_modificada = remesa_modificada 
        self.cantidad_solicitada = cantidad_solicitada
        
    def modificar_remesa(self, remesa):
        return
    