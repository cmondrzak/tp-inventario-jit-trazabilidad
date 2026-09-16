import proveedor
class gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos=movimientos
    def registrar_material(self,material):
        return
    def existencia_fisica():     #Es esteatico este?
        return
    def registrar_proveedor(self, id_proveedor, nombre, mail,telefono):
            # Falta validar: id_proveedor duplicado (IdentificadorDuplicadoError), ya hay un metodo que lo hace falta aplicarlo
            p = proveedor(id_proveedor, nombre,mail,telefono)
            self.proveedores.append(p)

    def existencia_disponible(): #lo mismo que en existencia fisica
        return
    def generar_pedido(id_pedido,proveedor,renglones,plazo_entrega,estado_pedido): #por ahi estaria bueno que estado pedido y renglones tengan valor por defecto al iniciar el pedido
        return
    def generar_retiro():
        return
    def obtener_pedidos(self,pedidos):  #lo veo medio inecesario a esto
        return pedidos