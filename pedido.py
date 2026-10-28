from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, PedidoNoEncontradoError, PlazoEntregaInvalidoError, DatoInvalidoError
from renglon_pedido import Renglon_pedido
from lista_enlazada import ListaEnlazada

class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega,estado): #Falta validar

        if not Validaciones.validarid(Pedido.lista_id,id_pedido):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")
        
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = ListaEnlazada()

        for renglon in renglones:
            self.renglones.agregar_final(renglon)

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
        return self._renglones.obtener_datos()
    
    def obtener_id_pedido(self):
        return self.id_pedido
    
    def __repr__(self):
        return f'{self.id_pedido},{self.proveedor},{self.obtener_renglones()},{self.plazo_entrega},{self.estado}'

    def generar_renglon(self,id_renglon,material,cantidad,precio_unitario):
        renglon = Renglon_pedido(id_renglon,material,cantidad,precio_unitario)
        self._renglones.agregar_final(renglon)

    def subtotal(self):
        sub_total=0

        for renglon in self.obtener_renglones():
            sub_total+=renglon.subtotal_renglon()
        return sub_total
    
    def eliminar_renglon_pedido(self,id_renglon):
        for renglon in self.obtener_renglones():
            if renglon.obtener_id_renglon() == id_renglon:
                self._renglones.eliminar(renglon)
                return

        raise ValueError("No existe un renglon con ese ID en el pedido.")
    
    def cambiar_estado(self,nuevo_estado):
        if nuevo_estado not in ["Pendiente", "En Proceso", "Completado"]:
            raise DatoInvalidoError("El estado ingresado no es válido. Debe ser 'Pendiente', 'En Proceso' o 'Completado'.")
        else: 
            self.estado=nuevo_estado