from movimiento import Movimiento
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError
import validaciones
class Movimiento_ingreso(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, remesa,pedido):   
        super().__init__(id_movimiento, fecha)
        if not Validaciones.es_no_vacio(remesa):
            raise ValueError("La remesa no puede estar vacía.")
        
        if not Validaciones.validarid(movimiento_ingreso.lista_id,self.id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.validar_fecha(self.fecha):
            raise FechaInvalidaError("Fecha invalida.")

        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.remesa = remesa    
        self.pedido=pedido
        movimiento_ingreso.lista_id.append(self.id_movimiento)

        
