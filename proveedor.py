from validaciones import Validaciones

from exceptions import IdentificadorDuplicadoError, NombreInvalidoError, PuntoDeReposicionInvalidoError, ProveedorNoEncontradoError, UnidadNoEncontradaError

class Proveedor:
    lista_id=[]
    def __init__(self, id_proveedor, nombre, mail,telefono):
        if not Validaciones.validarid(Proveedor.lista_id,id_proveedor):
                raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_no_vacio(id_proveedor):
            raise ProveedorNoEncontradoError("El proveedor no puede estar vacio")
        
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
        

    
