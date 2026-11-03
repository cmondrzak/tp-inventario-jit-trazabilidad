from validaciones import Validaciones
from exceptions import MaterialNoIndicadoError, CantidadARetirarNoPositivaError

class RenglonRetiro:
    def __init__(self, material, cantidad_solicitada):
        RenglonRetiro.validar_material(material)
        RenglonRetiro.validar_cantidad(cantidad_solicitada)

        self.material = material
        self.cantidad_solicitada = cantidad_solicitada

    @staticmethod
    def validar_material(material):
        if not Validaciones.es_texto_no_vacio(material):
            raise MaterialNoIndicadoError(f"Cada renglón del retiro tiene que indicar como texto qué material se retira; se recibió {material!r}.")

    @staticmethod
    def validar_cantidad(cantidad_solicitada):
        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadARetirarNoPositivaError(f"La cantidad a retirar debe ser mayor que cero; se pidió {cantidad_solicitada!r}.")

    def obtener_material(self):
        return self.material

    def obtener_cantidad_solicitada(self):
        return self.cantidad_solicitada

    @staticmethod
    def encabezado_resumen():
        return f"{'Material':<40}{'Cantidad':>14}"

    def linea_resumen(self):
        return f"{str(self.material)[:40]:<40}{self.cantidad_solicitada:>14}"
