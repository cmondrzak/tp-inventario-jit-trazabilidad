from validaciones import Validaciones
from exceptions import MaterialNoIndicadoError, CantidadARetirarNoPositivaError

class RenglonRetiro:
    def __init__(self, material, cantidad_solicitada):

        if not Validaciones.es_no_vacio(material):
            raise MaterialNoIndicadoError("Cada renglón del retiro tiene que indicar qué material se retira.")

        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadARetirarNoPositivaError(f"La cantidad a retirar debe ser mayor que cero; se pidió {cantidad_solicitada!r}.")

        self.material = material
        self.cantidad_solicitada = cantidad_solicitada
