from movimiento import Movimiento

class movimiento_retiro(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro):
        super().__init__(id_movimiento, fecha)
        self.renglones_retiro = renglones_retiro
        
    def agregar_renglon(self, renglon):
        self.renglones_retiro.append(renglon)
        
        