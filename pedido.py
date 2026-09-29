from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, PedidoNoEncontradoError, PlazoEntregaInvalidoError
from renglon_pedido import Renglon_pedido

class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega,estado): #Falta validar

        if not Validaciones.validarid(Pedido.lista_id,id_pedido):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        #Falta validar proveedor
        @staticmethod
        def es_renglonnovacio(renglones):
            if len(renglones) == 0:
                raise PedidoNoEncontradoError("El pedido debe tener al menos un renglón.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")
        
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = renglones
        self.plazo_entrega=plazo_entrega
        self.estado=estado
        Pedido.lista_id.append(self.id_pedido)

    def generar_renglon(self,id_renglon,material,cantidad,precio_unitario):
        r=Renglon_pedido(id_renglon,material,cantidad,precio_unitario)
        self.renglones.append(r)


    def subtotal(self):
        sub_total=0
        for objeto in self.renglones:
            sub_total+=objeto.subtotal_renglon()
        return sub_total

    def cambiar_estado(self,estado): #validar que solo puedan haber 3 estados, en proceso, aceptado, rechazado
        self.estado=estado
        return
    
        