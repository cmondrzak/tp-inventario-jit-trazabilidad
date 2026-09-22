from movimiento import Movimiento
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError

class Movimiento_retiro(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro):
        super().__init__(id_movimiento, fecha)
        if not Validaciones.validarid(Movimiento_retiro.lista_id,self.id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.validar_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")

        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.renglones_retiro = renglones_retiro
        
    def agregar_renglon(self, renglon):
        self.renglones_retiro.append(renglon)
        
        