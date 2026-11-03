from validaciones import Validaciones
from exceptions import IdentificadorDeMaterialInvalidoError, IdentificadorDeMaterialDuplicadoError, NombreDeMaterialVacioError, UnidadDeMedidaVaciaError, PuntoDeReposicionNoEnteroError, PuntoDeReposicionNoPositivoError, ExistenciaDisponibleInvalidaError


class Material:
    lista_id=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        Material.validar_id(id_material)
        Material.validar_nombre(nombre)
        Material.validar_unidad(unidad)
        Material.validar_punto_reposicion(punto_reposicion)

        self.id_material = id_material
        self.nombre = nombre
        self.unidad = unidad
        self.punto_reposicion = punto_reposicion

    @staticmethod
    def validar_id(id_material):
        if not Validaciones.es_identificador_valido(id_material):
            raise IdentificadorDeMaterialInvalidoError(f"El identificador del material debe ser un número entero positivo; se recibió {id_material!r}.")
        if not Validaciones.validarid(Material.lista_id,id_material):
            raise IdentificadorDeMaterialDuplicadoError(f"Ya existe un material con el identificador {id_material!r}; elegí otro identificador.")

    @staticmethod
    def validar_nombre(nombre):
        if not Validaciones.es_texto_no_vacio(nombre):
            raise NombreDeMaterialVacioError(f"El nombre del material es obligatorio y tiene que ser un texto; se recibió {nombre!r}.")

    @staticmethod
    def validar_unidad(unidad):
        if not Validaciones.es_texto_no_vacio(unidad):
            raise UnidadDeMedidaVaciaError(f"Hay que indicar la unidad de medida del material como texto (por ejemplo: kg, litros o unidades); se recibió {unidad!r}.")

    @staticmethod
    def validar_punto_reposicion(punto_reposicion):
        if not Validaciones.es_numero_entero(punto_reposicion):
            raise PuntoDeReposicionNoEnteroError(f"El punto de reposición tiene que ser un número entero, pero se recibió {punto_reposicion!r}.")
        if not Validaciones.es_positivo(punto_reposicion):
            raise PuntoDeReposicionNoPositivoError(f"El punto de reposición debe ser mayor que cero; se recibió {punto_reposicion}.")

    @classmethod
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
    
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id    
    
    def __repr__(self):
        return f'{self.id_material},{self.nombre},{self.unidad},{self.punto_reposicion}'
    

    def obtener_nombre(self):
        return self.nombre

    def requiere_reposicion(self, existencia_disponible):
        if not Validaciones.es_no_negativo(existencia_disponible):
            raise ExistenciaDisponibleInvalidaError(f"Para saber si hay que reponer, la existencia disponible debe ser un número mayor o igual a cero; se recibió {existencia_disponible!r}.")
        return existencia_disponible < self.punto_reposicion

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []
        
    def obtener_punto_reposicion(self):
        return self.punto_reposicion

    def obtener_unidad(self):
        return self.unidad