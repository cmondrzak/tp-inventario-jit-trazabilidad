from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError
import validaciones
class Movimiento_ingreso:
    lista_id=[]
    def __init__(self, id_movimiento, fecha, remesa,pedido):   
        if not Validaciones.es_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")

        if not Validaciones.es_no_vacio(remesa):
            raise ValueError("La remesa no puede estar vacía.")
        
        if not Validaciones.validarid(Movimiento_ingreso.lista_id,id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.remesa = remesa    
        self.pedido=pedido
        Movimiento_ingreso.lista_id.append(self.id_movimiento)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id

    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id
    
    def __repr__(self):
        return f'id = {self.id_movimiento}, fecha = {self.fecha}, remesa = {self.remesa}, pedido = {self.pedido}'

        
