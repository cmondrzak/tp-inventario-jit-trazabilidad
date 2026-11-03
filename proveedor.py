from validaciones import Validaciones

from exceptions import IdentificadorDeProveedorInvalidoError, IdentificadorDeProveedorDuplicadoError, NombreDeProveedorVacioError, PlazoDeEntregaNoPositivoError, CorreoElectronicoInvalidoError, NumeroDeTelefonoInvalidoError, ObjetoNoEsUnPedidoError, PedidoDeOtroProveedorError

from remesa import Remesa
from pedido import Pedido


class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, plazo_entrega, mail=None, telefono=None):
        Proveedor.validar_id(id_proveedor)
        Proveedor.validar_nombre(nombre)
        Proveedor.validar_plazo_entrega(plazo_entrega)
        Proveedor.validar_mail(mail)
        Proveedor.validar_telefono(telefono)

        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_entrega = plazo_entrega
        self.mail=mail
        self.telefono=telefono
        self.pedidos_pendientes = []

    @staticmethod
    def validar_id(id_proveedor):
        if not Validaciones.es_identificador_valido(id_proveedor):
            raise IdentificadorDeProveedorInvalidoError(f"El identificador del proveedor debe ser un número entero positivo; se recibió {id_proveedor!r}.")
        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
            raise IdentificadorDeProveedorDuplicadoError(f"Ya hay un proveedor registrado con el identificador {id_proveedor!r}.")

    @staticmethod
    def validar_nombre(nombre):
        if not Validaciones.es_texto_no_vacio(nombre):
            raise NombreDeProveedorVacioError(f"El nombre del proveedor es obligatorio y tiene que ser un texto; se recibió {nombre!r}.")

    @staticmethod
    def validar_plazo_entrega(plazo_entrega):
        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoDeEntregaNoPositivoError(f"El plazo de entrega del proveedor debe ser de al menos un día; se recibió {plazo_entrega!r}.")

    @staticmethod
    def validar_mail(mail):
        if mail is not None and not Validaciones.es_mail_valido(mail):
            raise CorreoElectronicoInvalidoError(f"La dirección de correo '{mail}' no es válida: tiene que tener la forma usuario@dominio.com y no puede llevar espacios.")

    @staticmethod
    def validar_telefono(telefono):
        if telefono is not None and not Validaciones.es_telefono_valido(telefono):
            raise NumeroDeTelefonoInvalidoError(f"El teléfono '{telefono}' no es válido: tiene que tener al menos 8 dígitos y solo puede llevar números, espacios, guiones y '+'.")

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
        return f'{self.id_proveedor},{self.nombre},{self.plazo_entrega},{self.mail},{self.telefono},{self.pedidos_pendientes}'
        
    def _validar_pedido_propio(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ObjetoNoEsUnPedidoError(f"Los pedidos pendientes de un proveedor tienen que ser pedidos, pero se recibió un objeto de tipo {type(pedido).__name__}.")
        if pedido.obtener_id_proveedor() != self.id_proveedor:
            raise PedidoDeOtroProveedorError(f"El pedido {pedido.obtener_id_pedido()} está dirigido al proveedor {pedido.obtener_id_proveedor()}, no al proveedor {self.id_proveedor}.")

    def agregar_pedido_pendiente(self,pedido):
        self._validar_pedido_propio(pedido)
        self.pedidos_pendientes.append(pedido)
        
    def obtener_idproveedor(self):
        return self.id_proveedor
    
    def obtener_pedidos_pendientes(self):
        return self.pedidos_pendientes

    @staticmethod
    def generar_remesa(id_remesa, material, id_proveedor, renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales):
        r = Remesa(id_remesa, material, id_proveedor, renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales)
        return r
    
    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []
    
    def eliminar_pedido_pendiente(self,id_pedido_pendiente):
        for pedido_pendiente in self.pedidos_pendientes:    
            if id_pedido_pendiente == pedido_pendiente.obtener_id_pedido():
                self.pedidos_pendientes.remove(pedido_pendiente)

    def guardar_pedidos_pendientes(self,pedidos):
        for pedido in pedidos:
            self._validar_pedido_propio(pedido)
        self.pedidos_pendientes = pedidos.copy()