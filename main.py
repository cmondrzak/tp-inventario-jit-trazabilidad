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
    def __init__(self, id_material, nombre, unidad, punto_reposicion, remesas):
        self.id_material = id_material
        self.nombre = nombre
        self.unidad = unidad
        self.punto_reposicion = punto_reposicion
        self.remesas = remesas
        
    def validar_reposicion(self):
        return
    
    def requiere_reposicion(self):
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


class Renglon:
    def __init__(self, material, cantidad, precio_unitario):
        self.material = material
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        
    def subtotal_renglon(self):
        return self.cantidad * self.precio_unitario

class Pedido:
    def __init__(self, id_pedido, proveedor, renglones):
        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self.renglones = renglones
        
    def agregar_renglon(self, renglon):
        self.renglones.append(renglon)
        
class Proveedor:
    def __init__(self, id_proveedor, nombre, plazo_entrega):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_entrega = plazo_entrega
        
    def entregar_material(self):
        return

