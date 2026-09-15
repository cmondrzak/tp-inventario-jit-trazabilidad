from movimiento import Movimiento

class Retiro(Movimiento):
    def __init__(self, id_movimiento, fecha, renglones_retiro):
        super().__init__(id_movimiento, fecha)
        self.renglones_retiro = renglones_retiro
        
    def agregar_renglon(self, renglon):
        self.remesas.append(renglon)
        