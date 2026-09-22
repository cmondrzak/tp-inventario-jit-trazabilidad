from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError

class Movimiento:
    lista_id=[]
    def __init__(self,id_movimiento, fecha):

        if not Validaciones.validarid(Movimiento.lista_id,self.id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        if not Validaciones.validar_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")
        
        self.id_movimiento = id_movimiento
        self.fecha = fecha
