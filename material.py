from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError
class Material:
    lista_id=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        self.id_material = Validaciones.validarid(id_material,self.idmateriales)

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        self.nombre = nombre
        self.unidad = unidad

        if not Validaciones.es_positivo(punto_reposicion):
            raise PuntoDeReposicionInvalidoError("El punto de reposición debe ser mayor que cero.")
        self.punto_reposicion = punto_reposicion
        Material.idmateriales.append(id_material)

    def validar_reposicion():
        return