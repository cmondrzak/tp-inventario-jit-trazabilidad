from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError

class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, pedidos_pendientes, mail,telefono):
        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
                    raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        
        self.nombre = nombre
        self.pedidios_pendientes = pedidos_pendientes
        self.mail=mail #falta validar mail
        self.telefono=telefono #validar telefono

    @staticmethod
    def validar_mail(mail):
        return mail
    @staticmethod
    def validar_telefono(telefono):
        return telefono
    def generar_remesa():
        return
    
    @staticmethod
    def cambiar_estado_pedido(pedido, nuevo_estado):
        pedido.cambiar_estado(nuevo_estado)
        
    def agregar_pedido_pendiente(self,pedido):
        self.pedidios_pendientes.append(pedido)
    
    def borrar_pedido_pendiente(self,pedido):
        self.pedidios_pendientes.remove(pedido)

        

        

    
