from movimiento import Movimiento
class movimiento_ingreso(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, remesa,pedido):    #tener remesa y pedido no es un poco redundante? yo pondira solo pedido, pero asi estaba en el UML
        super().__init__(id_movimiento, fecha)
        self.remesa = remesa    
        self.pedido=pedido     

        
