from movimiento import Movimiento
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError
class Movimiento_ingreso(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, remesa,pedido):    #tener remesa y pedido no es un poco redundante? yo pondira solo pedido, pero asi estaba en el UML
        super().__init__(id_movimiento, fecha)
        if not Validaciones.validarid(movimiento_ingreso.lista_id,self.id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        if not Validaciones.validar_fecha(self.fecha):
            raise FechaInvalidaError("La fecha no puede ser nula.")
        
        #Falta validar remesa
        
        
        self.remesa = remesa    
        self.pedido=pedido     

        
