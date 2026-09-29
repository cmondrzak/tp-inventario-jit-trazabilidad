from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError, UnidadNoEncontradaError, MaterialInvalidoError


class Material:
    lista_id=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        if not Validaciones.es_no_vacio(id_material):
            raise MaterialInvalidoError("El material no puede estar vacio")
        
        if not Validaciones.validarid(Material.lista_id,id_material):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        
        if not Validaciones.es_no_vacio(unidad):
            raise UnidadNoEncontradaError("La unidad no puede estar vacía.")

        if not Validaciones.es_positivo(punto_reposicion):
            raise PuntoDeReposicionInvalidoError("El punto de reposición debe ser mayor que cero.")
        
        self.id_material = id_material
        self.nombre = nombre
        self.unidad = unidad
        self.punto_reposicion = punto_reposicion
        Material.lista_id.append(self.id_material)

    def requiere_reposicion(self, existencia_disponible):
        return existencia_disponible < self.punto_reposicion

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []