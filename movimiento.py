from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError, FechaInvalidaError

class Movimiento:

    def __init__(self, fecha):
        
        if not Validaciones.es_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")
        
        self.fecha = fecha

        
    def __str__(self):
        return f"ID Movimiento:, Fecha: {self.fecha}"

    @classmethod
    def reiniciar_ids(cls):
        cls.lista_id = []

