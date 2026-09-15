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




class InventarioError(Exception):
    """Base de todo el dominio."""
    pass

# Nivel intermedio: identidad/colección
class IdentificadorDuplicadoError(InventarioError):
    pass

class EntidadNoEncontradaError(InventarioError):
    pass

class MaterialNoEncontradoError(EntidadNoEncontradaError):
    pass

class ProveedorNoEncontradoError(EntidadNoEncontradaError):
    pass

class RemesaNoEncontradaError(EntidadNoEncontradaError):
    pass

class ValorInvalidoError(InventarioError):
    pass

class NombreInvalidoError(ValorInvalidoError):
    pass

class PuntoDeReposicionInvalidoError(ValorInvalidoError):
    pass

class PlazoEntregaInvalidoError(ValorInvalidoError):
    pass

class CantidadInvalidaError(ValorInvalidoError):
    pass

class PrecioInvalidoError(ValorInvalidoError):
    pass

class SaldoInvalidoError(ValorInvalidoError):
    pass

class OperacionInvalidaError(InventarioError):
    pass

class ExistenciaInsuficienteError(OperacionInvalidaError):
    pass


class Material:
    materiales=[]
    def __init__(self, id_material, nombre, unidad, punto_reposicion):
        self.id_material = Material.validarid(id_material)

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        self.nombre = nombre
        self.unidad = unidad

        if not Validaciones.es_positivo(punto_reposicion):
            raise PuntoDeReposicionInvalidoError("El punto de reposición debe ser mayor que cero.")
        self.punto_reposicion = punto_reposicion

        Material.materiales.append(id_material)

    @staticmethod
    def validarid(id_material):
        if id_material in Material.materiales:
            raise IdentificadorDuplicadoError(f"Material {id_material} ya registrado.")
        else:
           return id_material

class Remesa:
    def __init__(self, id_remesa, material, proveedor, cantidad_recibida, saldo_disponible, fecha_recepcion, fecha_vencimiento, precio_unitario):
        self.id_remesa = id_remesa
        self.material = material
        self.proveedor = proveedor

        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadInvalidaError("La cantidad recibida debe ser mayor que cero.")
        self.cantidad_recibida = cantidad_recibida

        # Falta validar: saldo_disponible no negativo y no mayor a cantidad_recibida (RN10, RN11)
        self.saldo_disponible = saldo_disponible

        self. fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioInvalidoError("El precio unitario debe ser mayor que cero.")
        self.precio_unitario = precio_unitario
        
    def es_utilizable(self, fecha):
        # Falta validar (RN17)
        return
    
    def vencida(self, fecha):
        # Falta validar (RN17)
        return
    
    def consumir(self, cantidad):
        # Falta validar: cantidad positiva y cantidad <= saldo_disponible (SaldoInvalidoError)
        return

    def movimientos(self):
        return
    
    def validarid():
        return


class Renglon:
    def __init__(self, material, cantidad, precio_unitario):
        self.material = material

        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero.")
        self.cantidad = cantidad

        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioInvalidoError("El precio unitario debe ser mayor que cero.")
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

        if not Validaciones.es_no_vacio(nombre):
            raise NombreInvalidoError("El nombre no puede estar vacío.")
        self.nombre = nombre

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoEntregaInvalidoError("El plazo de entrega debe ser mayor que cero.")
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
        self.renglones_retiro.append(renglon)
        
class RenglonRetiro:
    def __init__(self, material, remesa_modificada, cantidad_solicitada):
        self.material = material
        self.remesa_modificada = remesa_modificada

        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadInvalidaError("La cantidad solicitada debe ser mayor que cero.")
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
        # Falta validar: id_material duplicado (IdentificadorDuplicadoError)
        m = Material(id_material, nombre, unidad_medida, punto_reposicion)
        self.materiales.append(m)
        

    def registrar_proveedor(self, id_proveedor, nombre, plazo_de_entrega):
        # Falta validar: id_proveedor duplicado (IdentificadorDuplicadoError)
        p = Proveedor(id_proveedor, nombre, plazo_de_entrega)
        self.proveedores.append(p)

    def obtener_material(self, id_material):
        # Falta validar: material no encontrado (MaterialNoEncontradoError)
        return

    def obtener_proveedor(self, id_proveedor):
        # Falta validar: proveedor no encontrado (ProveedorNoEncontradoError)
        return

    def obtener_remesa(self, id_remesa):
        # Falta validar: remesa no encontrada (RemesaNoEncontradaError)
        return

    def existencia_fisica(self, id_material):
        return
    
    def existencia_disponible(self, id_material, fecha):
        return
    
    def generar_retiro(self, id_material, cantidad_solicitada, fecha):
        if not Validaciones.es_positivo(cantidad_solicitada):
            raise CantidadInvalidaError("La cantidad a retirar debe ser mayor que cero.")
        # Falta validar: existencia disponible suficiente (ExistenciaInsuficienteError, RN18)
        return
    
    def generar_ingreso(self):
        return
    
    def almacenar_remesa(self, id_remesa, id_material, id_proveedor, cantidad_recibida,
                          fecha_recepcion, fecha_vencimiento, precio_unitario):
        # Falta validar: id_remesa duplicado (IdentificadorDuplicadoError)
        # Falta validar: material existente (MaterialNoEncontradoError)
        # Falta validar: proveedor existente (ProveedorNoEncontradoError)
        return

#Validaciones
class Validaciones:
    @staticmethod
    def es_positivo(valor):
        return valor is not None and valor > 0

    @staticmethod
    def es_no_vacio(texto):
        return texto is not None and texto.strip() != ""