from validaciones import Validaciones
from exceptions import IdentificadorDeRenglonDePedidoDuplicadoError, MaterialNoIndicadoError, CantidadPedidaNoEnteraError, CantidadPedidaNoPositivaError, PrecioUnitarioNoPositivoError

class Renglon_pedido:
    lista_id=[]
    def __init__(self,id_renglon ,material, cantidad, precio_unitario):
        if not Validaciones.validarid(Renglon_pedido.lista_id,id_renglon):
            raise IdentificadorDeRenglonDePedidoDuplicadoError(f"Ya existe un renglón de pedido con el identificador {id_renglon!r}.")

        if not isinstance(material, str) or not Validaciones.es_no_vacio(material):
            raise MaterialNoIndicadoError(f"El renglón tiene que indicar el nombre del material como texto; se recibió {material!r}.")

        if not Validaciones.es_numero_entero(cantidad):
            raise CantidadPedidaNoEnteraError(f"La cantidad pedida tiene que ser un número entero; se recibió {cantidad!r}.")

        if not Validaciones.es_positivo(cantidad):
            raise CantidadPedidaNoPositivaError(f"La cantidad pedida debe ser mayor que cero; se recibió {cantidad}.")

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioUnitarioNoPositivoError(f"El precio unitario acordado debe ser mayor que cero; se recibió {precio_unitario!r}.")

        self.id_renglon=id_renglon
        self.material = material
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.ingresado = False
        Renglon_pedido.lista_id.append(self.id_renglon)
        
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

    def subtotal_renglon(self):
        return self.cantidad * self.precio_unitario
    
    def obtener_id_renglon_pedido(self):
        return self.id_renglon
    
    def obtener_material(self):
        return self.material
    
    def obtener_cantidad(self):
        return self.cantidad

    def obtener_precio_unitario(self):
        return self.precio_unitario

    