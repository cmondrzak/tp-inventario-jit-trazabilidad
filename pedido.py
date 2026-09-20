class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega,estado): #Falta validar
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = renglones
        self.plazo_entrega=plazo_entrega
        self.estado=estado

    def subtotal():
        return
    def generar_renglon(self, renglon):
        self.renglones.append(renglon)
    def cambiar_estado():
        return

        