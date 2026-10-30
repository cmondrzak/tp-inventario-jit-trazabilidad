from validaciones import Validaciones

from exceptions import IdentificadorDeProveedorInvalidoError, IdentificadorDeProveedorDuplicadoError, NombreDeProveedorVacioError, PlazoDeEntregaNoPositivoError, CorreoElectronicoInvalidoError, NumeroDeTelefonoInvalidoError

from remesa import Remesa


class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, plazo_entrega, mail=None, telefono=None):
        if not Validaciones.es_identificador_valido(id_proveedor):
            raise IdentificadorDeProveedorInvalidoError(f"El identificador del proveedor debe ser un número entero positivo o un texto con contenido; se recibió {id_proveedor!r}.")

        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
            raise IdentificadorDeProveedorDuplicadoError(f"Ya hay un proveedor registrado con el identificador {id_proveedor!r}.")

        if not Validaciones.es_no_vacio(nombre):
            raise NombreDeProveedorVacioError("El nombre del proveedor es obligatorio y no puede quedar en blanco.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoDeEntregaNoPositivoError(f"El plazo de entrega del proveedor debe ser de al menos un día; se recibió {plazo_entrega!r}.")

        if mail is not None and not Validaciones.es_mail_valido(mail):
            raise CorreoElectronicoInvalidoError(f"La dirección de correo '{mail}' no es válida: tiene que tener la forma usuario@dominio.com y no puede llevar espacios.")

        if telefono is not None and not Validaciones.es_telefono_valido(telefono):
            raise NumeroDeTelefonoInvalidoError(f"El teléfono '{telefono}' no es válido: tiene que tener al menos 8 dígitos y solo puede llevar números, espacios, guiones y '+'.")

        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_entrega = plazo_entrega
        self.mail=mail
        self.telefono=telefono
        self.pedidos_pendientes = []
        Proveedor.lista_id.append(self.id_proveedor)
    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
    
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id

    def __repr__(self):
        return f'{self.id_proveedor},{self.nombre},{self.plazo_entrega},{self.mail},{self.telefono},{self.pedidos_pendientes}'
        
    def agregar_pedido_pendiente(self,pedido):
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