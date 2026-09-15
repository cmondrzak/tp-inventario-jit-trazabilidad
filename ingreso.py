from movimiento import Movimiento

class Ingreso(Movimiento):
    def __init__(self, id_movimiento, fecha, remesa):
        super().__init__(id_movimiento, fecha)
        self.remesa = remesa 
        
