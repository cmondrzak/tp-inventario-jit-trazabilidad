from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError
class Material:
    lista_id=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        
        if not Validaciones.validarid(Material.lista_id,self.id_material):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        

        if not Validaciones.es_positivo(punto_reposicion):
            raise PuntoDeReposicionInvalidoError("El punto de reposición debe ser mayor que cero.")
        
        self.id_material = id_material
        self.nombre = nombre
        self.unidad = unidad
        self.punto_reposicion = punto_reposicion
        Material.lista_id.append(self.id_material)
        

    def validar_reposicion():
        return