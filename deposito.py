from datetime import date

from proveedor import Proveedor

from material import Material

from remesa import Remesa

from validaciones import Validaciones

from exceptions import ObjetoNoEsUnaRemesaError, ObjetoNoEsUnMaterialError, IdentificadorDeRemesaDuplicadoError, IdentificadorDeMaterialDuplicadoError, IdentificadorDeMaterialNoCoincideConLaClaveError





class Deposito:
    def __init__(self,remesas, materiales):
        self.remesas = remesas
        self.materiales = materiales
    
    # def retirar(retiro, metodo_descarga):
    #     metodo_descarga(retiro)
    
    def almacenar_remesa(self,remesa):
        if not isinstance(remesa, Remesa):
            raise ObjetoNoEsUnaRemesaError(f"El depósito solo puede almacenar remesas, pero recibió un objeto de tipo {type(remesa).__name__}.")
        clave = str(remesa.obtener_id_remesa())
        # La clave es str(id): 1 y "1" chocarian y se perderia una remesa
        if clave in self.remesas:
            raise IdentificadorDeRemesaDuplicadoError(f"El depósito ya tiene almacenada una remesa con el identificador {clave!r}; guardar otra con el mismo identificador haría perder la anterior.")
        self.remesas[clave] = remesa

    def modificar_materiales(self,material,id_material):
        if not isinstance(material, Material):
            raise ObjetoNoEsUnMaterialError(f"En el depósito solo se pueden registrar materiales, pero se recibió un objeto de tipo {type(material).__name__}.")
        if material.id_material != id_material:
            raise IdentificadorDeMaterialNoCoincideConLaClaveError(f"Se intentó guardar el material {material.id_material!r} bajo el identificador {id_material!r}; los dos tienen que ser iguales.")
        if id_material in self.materiales:
            raise IdentificadorDeMaterialDuplicadoError(f"El depósito ya tiene registrado un material con el identificador {id_material!r}.")
        self.materiales[id_material]=material
        return
    def obtener_remesas(self):
        return self.remesas
    
    def validar_reposicion(self,id_material):
        return
    
    def obtener_materiales(self):
        return self.materiales.copy()
    
    def remesas_por_material(self, material, fecha):
        disponibles = []

        for remesa in self.remesas.values():
            if (remesa.obtener_material() == material and remesa.es_utilizable(fecha)):
                disponibles.append(remesa)

        return disponibles

    
    @staticmethod
    def retirar_fefo(remesas):
        def criterio(remesa):
            return remesa.clave_fefo()

        return sorted(remesas, key=criterio)
    