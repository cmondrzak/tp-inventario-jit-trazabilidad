# # Tu implementacion va aqui
# def hola_mundo():
#     return "hola_mundo"


# def main():
#     # Aqui ejecutas tus soluciones
#     print(hola_mundo())


# # No cambiar a partir de aqui
# if __name__ == "__main__":
#     main()

import random
import time

class Material:
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        self.id_material = id_material
        self.nombre = nombre
        self.unidad = unidad
        self.punto_reposicion = punto_reposicion
        
    def validar_reposicion(self):
        return
    def validarid():

        return

    

class Remesa:
    def __init__(self, id_remesa, material, proveedor, cantidad_recibida, saldo_disponible, fecha_recepcion, fecha_vencimiento, precio_unitario):
        self.id_remesa = id_remesa
        self.material = material
        self.proveedor = proveedor
        self.cantidad_recibida = cantidad_recibida
        self.saldo_disponible = saldo_disponible
        self. fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        self.precio_unitario = precio_unitario
        
    def es_utilizable(self):
        return
    
    def vencida(self):
        return
    
    def validar_cantidad_recibida(self):
        return
    
    def movimientos(self):
        return
    def validarid():
        return
    @staticmethod
    def validarMayorCero(num):
        return


class Renglon:
    def __init__(self, material, cantidad, precio_unitario):
        self.material = material
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        
    def subtotal_renglon(self):
        return self.cantidad * self.precio_unitario
    def validarid():
        return


class Pedido:
    def __init__(self, id_pedido, proveedor, renglones):
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = renglones
        
    def agregar_renglon(self, renglon):
        self.renglones.append(renglon)
    def validarid():
        return
        
class Proveedor:
    def __init__(self, id_proveedor, nombre, plazo_entrega):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_entrega = plazo_entrega
        
    def entregar_material(self):
        return
    def validarid():
        return

class Movimiento:
    def __init__(self,id_movimiento, fecha):
        self.id_movimiento = id_movimiento
        self.fecha = fecha
    def validarid():
        return

    
    
class Ingreso(Movimiento):
    def __init__(self, id_movimiento, fecha, remesa):
        super().__init__(id_movimiento, fecha)
        self.remesa = remesa 
        

class Retiro(Movimiento):
    def __init__(self, id_movimiento, fecha, renglones_retiro):
        super().__init__(id_movimiento, fecha)
        self.renglones_retiro = renglones_retiro
        
    def agregar_renglon(self, renglon):
        self.remesas.append(renglon)
        
class RenglonRetiro:
    def __init__(self, material, remesa_modificada, cantidad_solicitada):
        self.material = material
        self.remesa_modificada = remesa_modificada
        self.cantidad_solicitada = cantidad_solicitada
        
    def modificar_remesa(self, remesa):
        return
    

class Deposito:
    def __init__(self,id_deposito ,remesas, retiros, politicas, materiales, proveedores, movimientos):
        self.id_deposito=id_deposito
        self.remesas = remesas
        self.retiros = retiros
        self.politicas = politicas
        self.materiales = materiales
        self.proveedores = proveedores
        self.movimientos = movimientos
        
    def registrar_material(self, id_material, nombre, unidad_medida, punto_reposicion):
        m = Material(id_material, nombre, unidad_medida, punto_reposicion)
        self.materiales.append(m)
        

    def registrar_proveedor(self, id_proveedor, nombre, plazo_de_entrega):
        p = Proveedor(id_proveedor, nombre, plazo_de_entrega)
        self.proveedores.append(p)
    def validarid():
        return
        
    def existencia_fisica(self):
        return
    
    def existencia_disponible(self):
        return
    
    def generar_retiro(self):
        return
    
    def generar_ingreso(self):
        return
    
    def almacenar_remesa(self):
        return
    
