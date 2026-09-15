from proveedor import Proveedor

from material import Material

from validaciones import Validaciones

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
    
    def generar_retiro(self, cantidad_solicitada):
        if not Validaciones.es_positivo(cantidad_solicitada):
            raise ValueError("La cantidad a retirar debe ser mayor que cero.")
        return
    
    def generar_ingreso(self):
        return
    
    def almacenar_remesa(self):
        return
    