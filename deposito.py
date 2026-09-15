from proveedor import Proveedor

from material import Material

from remesa import Remesa

from retiro import Retiro

from validaciones import Validaciones

from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError, RemesaNoEncontradaError, ExistenciaInsuficienteError



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
