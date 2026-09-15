from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError, PlazoEntregaInvalidoError

class Proveedor:
    def __init__(self, id_proveedor, nombre, plazo_entrega):
        self.id_proveedor = id_proveedor

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        self.nombre = nombre

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")
        self.plazo_entrega = plazo_entrega
        
    def entregar_material(self):
        return
    def validarid():
        return

    
