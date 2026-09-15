from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError

class Material:
    materiales=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        self.id_material = Material.validarid(id_material)

        if not Validaciones.es_no_vacio(nombre):
            raise ValueError("El nombre no puede estar vacío.")
        self.nombre = nombre

        self.unidad = unidad

        if not Validaciones.es_positivo(punto_reposicion):
            raise ValueError("El punto de reposición debe ser mayor que cero.")
        self.punto_reposicion = punto_reposicion

        Material.materiales.append(id_material)

    @staticmethod
    def validarid(id_material):
            if id_material in Material.materiales:
                raise IdentificadorDuplicadoError(f"Material {id_material} ya registrado.")
            else:
               return id_material
           
