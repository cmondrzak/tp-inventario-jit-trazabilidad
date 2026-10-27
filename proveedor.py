from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, DatoInvalidoError, PlazoEntregaInvalidoError, PuntoDeReposicionInvalidoError, UnidadNoEncontradaError

from remesa import Remesa


class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, plazo_entrega, mail=None, telefono=None):
        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")

        if mail is not None and not Validaciones.es_mail_valido(mail):
            raise DatoInvalidoError("El correo electrónico no es válido.")

        if telefono is not None and not Validaciones.es_telefono_valido(telefono):
            raise DatoInvalidoError("El número de teléfono no es válido.")

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