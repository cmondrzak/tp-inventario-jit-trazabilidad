from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, PedidoNoEncontradoError, PlazoEntregaInvalidoError, DatoInvalidoError
from renglon_pedido import Renglon_pedido

class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega,estado): #Falta validar

        if not Validaciones.validarid(Pedido.lista_id,id_pedido):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")
        
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = renglones
        self.plazo_entrega=plazo_entrega
        self.estado=estado
        Pedido.lista_id.append(self.id_pedido)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
    
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id
    
    def obtener_renglones(self):
        return self.renglones
    
    def obtener_id_pedido(self):
        return self.id_pedido
    
    def __repr__(self):
        return f'{self.id_pedido},{self.proveedor},{self.renglones},{self.plazo_entrega},{self.estado}'

    def generar_renglon(self,id_renglon,material,cantidad,precio_unitario):
        r=Renglon_pedido(id_renglon,material,cantidad,precio_unitario)
        self.renglones.append(r)

    def subtotal(self):
        sub_total=0
        for objeto in self.renglones:
            sub_total+=objeto.subtotal_renglon()
        return sub_total
    
    def eliminar_renglon_pedido(self,id_renglon):
        for renglon in self.renglones:
            if renglon.id_renglon == id_renglon:
                self.renglones.remove(renglon)
    
    def cambiar_estado(self,nuevo_estado):
        if nuevo_estado not in ["Pendiente", "En Proceso", "Completado"]:
            raise DatoInvalidoError("El estado ingresado no es válido. Debe ser 'Pendiente', 'En Proceso' o 'Completado'.")
        else: 
            self.estado=nuevo_estado