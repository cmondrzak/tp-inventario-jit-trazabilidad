import datetime
from proveedor import Proveedor
from pedido import Pedido
from material import Material
from deposito import Deposito
from movimiento_retiro import Movimiento_retiro
from movimiento_ingreso import Movimiento_ingreso
from validaciones import Validaciones
from remesa import Remesa
from exceptions import PedidoNoEncontradoError
class Gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos=movimientos

    def registrar_material(self,id_material,nombre,unidad_medida,reposicion):
        m=Material(id_material,nombre,unidad_medida,reposicion)
        self.deposito[0].modificar_materiales(m,id_material)

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
        
    def registrar_proveedor(self, id_proveedor, nombre, plazo_entrega , mail,telefono):
            p = Proveedor(id_proveedor, nombre,plazo_entrega,mail = mail,telefono = telefono)
            self.proveedores[id_proveedor]=p

    @staticmethod
    def existencia_disponible(deposito,material):
         rem = deposito.obtener_remesas()
         cantidad_total=0
         for clave,valor in rem.items():
              if valor.obtener_material()==material and valor.fecha_vencimiento>=datetime.datetime.today():
                   cantidad_total+=valor.obtener_cantidad_recibida()
         return cantidad_total
        
    def generar_pedido(self,id_pedido,proveedor,renglones,plazo_entrega): #por ahi estaria bueno que estado pedido y renglones tengan valor por defecto al iniciar el pedido
        p=Pedido(id_pedido,proveedor,renglones,plazo_entrega,"Solicitado")
        self.pedidos[id_pedido] = p
        self.proveedores[proveedor].agregar_pedido_pendiente(p)
        

    def generar_retiro(self,id_movimiento,fecha,renglones,metodo_descarga): # metodo_retiro es la politica de descarga
        r = Movimiento_retiro(id_movimiento,fecha,renglones)
        self.movimientos[id_movimiento]=r
        self.deposito.retirar(r,metodo_descarga)

    def obtener_pedidos(self):
        return self.pedidos
    
    def obtener_proveedores(self):
        return self.proveedores
    
    def obtener_movimientos(self):
        return self.movimientos
    
    def almacenar_remesa(self,id_movimiento_ingreso, id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales):
        r = Proveedor.generar_remesa(id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales)
        for pedido in self.proveedores[id_proveedor].obtener_pedidos_pendientes():
            for renglon in pedido.obtener_renglones():
                if r.obtener_id_renglon_pedido() == renglon.obtener_id_renglon_pedido():
                    m = Movimiento_ingreso(id_movimiento_ingreso, fecha_recepcion, id_remesa, pedido.obtener_id_pedido())
                    self.movimientos[id_movimiento_ingreso] = m
                    self.deposito[0].almacenar_remesa(r)
                    return
        raise PedidoNoEncontradoError 
        return
    