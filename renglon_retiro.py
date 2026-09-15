from validaciones import Validaciones
from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError

class RenglonRetiro:
    def __init__(self, material, remesa_modificada, cantidad_solicitada):
        self.material = material
        self.remesa_modificada = remesa_modificada

        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadInvalidaError("La cantidad solicitada debe ser mayor que cero.")
        self.cantidad_solicitada = cantidad_solicitada
        
    def modificar_remesa(self, remesa):
        return
    