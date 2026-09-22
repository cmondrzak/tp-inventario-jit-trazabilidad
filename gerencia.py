import datetime
from proveedor import Proveedor
from pedido import Pedido
from material import Material
from deposito import Deposito
from movimiento_retiro import Movimiento_retiro
class Gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos=movimientos

    def registrar_material(self,id_material,nombre,unidad_medida,reposicion,deposito):
        m=Material(id_material,nombre,unidad_medida,reposicion)
        deposito.modificar_materiales(m,id_material)

    def crear_deposito(self,remesas,materiales):
         d=Deposito(remesas,materiales)
         self.deposito.append(d)

    @staticmethod
    def existencia_fisica(deposito,material):
         rem = deposito.obtener_remesas()
         cantidad_total=0
         for clave,valor in rem.items():
              if valor.obtener_material()==material:
                   cantidad_total+=valor.obtener_cantidad_recibida()
         return cantidad_total
        
    def registrar_proveedor(self, id_proveedor, nombre, mail,telefono):
            p = Proveedor(id_proveedor, nombre,mail,telefono)
            self.provedores[id_proveedor]=p

    @staticmethod
    def existencia_disponible(deposito,material):
         rem = deposito.obtener_remesas()
         cantidad_total=0
         for clave,valor in rem.items():
              if valor.obtener_material()==material and valor.fecha_vencimiento>=datetime.datetime.today():
                   cantidad_total+=valor.obtener_cantidad_recibida()
         return cantidad_total
        
    def generar_pedido(self,id_pedido,proveedor,renglones,plazo_entrega,estado_pedido): #por ahi estaria bueno que estado pedido y renglones tengan valor por defecto al iniciar el pedido
        p=Pedido(id_pedido,proveedor,renglones,plazo_entrega,estado_pedido)
        self.pedidos[id_pedido] = p
        return

    def generar_retiro(self,id_movimiento,fecha,renglones):
        r = Movimiento_retiro(id_movimiento,fecha,renglones)
        self.movimientos[id_movimiento]=r

    def obtener_pedidos(self):
        return self.pedidos