from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError, PlazoEntregaInvalidoError

class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, mail,telefono):
        self.id_proveedor = id_proveedor #falta validarid

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        self.nombre = nombre
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
    def cambiar_estado_pedido():
        return
        

    
