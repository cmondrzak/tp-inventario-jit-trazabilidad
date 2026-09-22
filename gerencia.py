from proveedor import Proveedor
from pedido import Pedido
from material import Material
from deposito import Deposito
class Gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos=movimientos
    def registrar_material(self,id_material,nombre,unidad_medida,reposicion,deposito):
        m=Material(id_material,nombre,unidad_medida,reposicion)
        deposito.modificar_materiales(m,id_material)
    
    def existencia_fisica(deposito):
         return
        
    def registrar_proveedor(self, id_proveedor, nombre, mail,telefono):
            p = Proveedor(id_proveedor, nombre,mail,telefono)
            self.provedores[id_proveedor]=p

    def existencia_disponible(): #lo mismo que en existencia fisica
        return
    def generar_pedido(self,id_pedido,proveedor,renglones,plazo_entrega,estado_pedido): #por ahi estaria bueno que estado pedido y renglones tengan valor por defecto al iniciar el pedido
        p=Pedido(id_pedido,proveedor,renglones,plazo_entrega,estado_pedido)
        self.pedidos[id_pedido] = p
        
        return
    def generar_retiro():
        return
    def obtener_pedidos(self,pedidos):  #lo veo medio inecesario a esto
        return pedidos