from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, DatoInvalidoError, PlazoEntregaInvalidoError, PuntoDeReposicionInvalidoError, UnidadNoEncontradaError

class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, plazo_entrega, mail=None, telefono=None):
        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")

        if not Validaciones.validar_plazo_entrega(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")

        if mail is not None and not Validaciones.validar_mail(mail):
            raise DatoInvalidoError("El correo electrónico no es válido.")

        if telefono is not None and not Validaciones.validar_telefono(telefono):
            raise DatoInvalidoError("El número de teléfono no es válido.")

        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_entrega = plazo_entrega
        self.mail=mail
        self.telefono=telefono
        self.pedidos_pendientes = []
        Proveedor.lista_id.append(self.id_proveedor)


    @staticmethod
    def cambiar_estado_pedido(pedido, nuevo_estado):
        pedido.cambiar_estado(nuevo_estado)
        
    def agregar_pedido_pendiente(self,pedido):
        self.pedidios_pendientes.append(pedido)
    
    def borrar_pedido_pendiente(self,pedido):
        self.pedidios_pendientes.remove(pedido)

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []