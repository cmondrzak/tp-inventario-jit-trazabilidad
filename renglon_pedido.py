from validaciones import Validaciones
from exceptions import IdentificadorDeRenglonDePedidoInvalidoError, IdentificadorDeRenglonDePedidoDuplicadoError, MaterialNoIndicadoError, CantidadPedidaNoEnteraError, CantidadPedidaNoPositivaError, MaterialRecibidoDistintoDelPedidoError, CantidadRecibidaDistintaDeLaPedidaError

class Renglon_pedido:
    lista_id=[]
    def __init__(self,id_renglon ,material, cantidad):
        Renglon_pedido.validar_id(id_renglon)
        Renglon_pedido.validar_material(material)
        Renglon_pedido.validar_cantidad(cantidad)

        self.id_renglon=id_renglon
        self.material = material
        self.cantidad = cantidad
        self.ingresado = False

    @staticmethod
    def validar_id(id_renglon):
        if not Validaciones.es_identificador_valido(id_renglon):
            raise IdentificadorDeRenglonDePedidoInvalidoError(f"El identificador del renglón de pedido debe ser un número entero positivo; se recibió {id_renglon!r}.")
        if not Validaciones.validarid(Renglon_pedido.lista_id,id_renglon):
            raise IdentificadorDeRenglonDePedidoDuplicadoError(f"Ya existe un renglón de pedido con el identificador {id_renglon!r}.")

    @staticmethod
    def validar_material(material):
        if not Validaciones.es_texto_no_vacio(material):
            raise MaterialNoIndicadoError(f"El renglón tiene que indicar el nombre del material como texto; se recibió {material!r}.")

    @staticmethod
    def validar_cantidad(cantidad):
        if not Validaciones.es_numero_entero(cantidad):
            raise CantidadPedidaNoEnteraError(f"La cantidad pedida tiene que ser un número entero; se recibió {cantidad!r}.")
        if not Validaciones.es_positivo(cantidad):
            raise CantidadPedidaNoPositivaError(f"La cantidad pedida debe ser mayor que cero; se recibió {cantidad}.")

    def validar_material_recibido(self, material):
        if Validaciones.normalizar_texto(material) != Validaciones.normalizar_texto(self.material):
            raise MaterialRecibidoDistintoDelPedidoError(f"Se recibió '{material}', pero el renglón {self.id_renglon!r} del pedido solicitaba '{self.material}'.")

    def validar_cantidad_recibida(self, cantidad):
        if cantidad != self.cantidad:
            raise CantidadRecibidaDistintaDeLaPedidaError(f"El renglón {self.id_renglon!r} del pedido solicitaba {self.cantidad}, pero se recibieron {cantidad}; la cantidad recibida tiene que coincidir con la pedida.")

    @classmethod
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
        
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id

    def modificar_ingresado(self):
        self.ingresado = True

    def obtener_ingresado(self):
        return self.ingresado

    def obtener_id_renglon_pedido(self):
        return self.id_renglon
    
    def obtener_material(self):
        return self.material
    
    def obtener_cantidad(self):
        return self.cantidad

    