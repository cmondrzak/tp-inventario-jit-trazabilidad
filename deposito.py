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
        self.remesas_agotadas = {}
    
    # def retirar(retiro, metodo_descarga):
    #     metodo_descarga(retiro)

    def almacenar_remesa(self,remesa):
        if not isinstance(remesa, Remesa):
            raise ObjetoNoEsUnaRemesaError(f"El depósito solo puede almacenar remesas, pero recibió un objeto de tipo {type(remesa).__name__}.")
        clave = str(remesa.obtener_id_remesa())
        # La clave es str(id): 1 y "1" chocarian y se perderia una remesa
        if clave in self.remesas or clave in self.remesas_agotadas:
            raise IdentificadorDeRemesaDuplicadoError(f"El depósito ya tiene almacenada una remesa con el identificador {clave!r}; guardar otra con el mismo identificador haría perder la anterior.")
        if remesa.obtener_saldo()==0:
            self.remesas_agotadas[clave] = remesa
        else:
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
        return self.remesas.copy()
    def obtener_remesas_agotadas(self):
        return self.remesas_agotadas.copy()
    
    def obtener_todas_las_remesas(self):
        todas = self.remesas.copy()
        todas.update(self.remesas_agotadas)
        return todas
    def obtener_remesa(self,id_remesa):
        clave = str(id_remesa)

        if clave in self.remesas:
            return self.remesas[clave]

        return self.remesas_agotadas[clave]

    def archivar_remesa_agotada(self,remesa):
        clave = str(remesa.obtener_id_remesa())

        if remesa.obtener_saldo()==0 and clave in self.remesas:
            self.remesas_agotadas[clave] = self.remesas[clave]
            del self.remesas[clave]

    def actualizar_remesas_guardadas(self):
        if not hasattr(self,"remesas_agotadas"):
            self.remesas_agotadas = {}

        claves_agotadas = []

        for clave, remesa in self.remesas.items():
            if remesa.obtener_saldo()==0:
                claves_agotadas.append(clave)

        for clave in claves_agotadas:
            self.remesas_agotadas[clave] = self.remesas[clave]
            del self.remesas[clave]
        
    def validar_reposicion(self,id_material):
        material = self.materiales[id_material]

        existencia = self.existencia_disponible(
            material.obtener_nombre()
        )

        return material.requiere_reposicion(existencia)
    
    def obtener_materiales(self):
        return self.materiales.copy()
    
    def remesas_por_material(self, material, fecha):
        disponibles = []

        for remesa in self.remesas.values():
            if (remesa.obtener_material() == material and remesa.es_utilizable(fecha)):
                disponibles.append(remesa)

        return disponibles

    def existencia_disponible(self,nombre):
        nombre = Validaciones.normalizar_texto(nombre)
        existencia = 0

        for remesa in self.remesas_por_material(nombre,date.today()):
            existencia += remesa.obtener_saldo()

        return existencia
    
    @staticmethod
    def retirar_fefo(remesas):
        def criterio(remesa):
            return remesa.clave_fefo()

        return sorted(remesas, key=criterio)

    def obtener_materiales_a_reponer(self):
        materiales_a_reponer = []

        for id_material in self.materiales:
            datos = self.obtener_datos_reposicion(id_material)

            if datos["requiere_reposicion"]:
                materiales_a_reponer.append(datos)

        return materiales_a_reponer

    def obtener_datos_reposicion(self,id_material):
        material = self.materiales[id_material]

        existencia = self.existencia_disponible(
            material.obtener_nombre()
        )

        punto = material.obtener_punto_reposicion()

        return {
            "id_material": id_material,
            "nombre": material.obtener_nombre(),
            "unidad": material.obtener_unidad(),
            "existencia": existencia,
            "punto_reposicion": punto,
            "diferencia": existencia-punto,
            "requiere_reposicion": material.requiere_reposicion(existencia)
        }
    