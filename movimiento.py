from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError

class Movimiento:
    lista_id=[]
    def __init__(self,id_movimiento, fecha):
        if not Validaciones.validarid(Movimiento.lista_id,id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")
        
        if not Validaciones.es_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")
        
        self.id_movimiento = id_movimiento
        self.fecha = fecha
        Movimiento.lista_id.append(self.id_movimiento)

    def __str__(self):
        return f"ID Movimiento: {self.id_movimiento}, Fecha: {self.fecha}"

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []
