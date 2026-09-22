from proveedor import Proveedor

from material import Material

from remesa import Remesa

from movimiento_retiro import movimiento_retiro

from validaciones import Validaciones

from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError, RemesaNoEncontradaError, ExistenciaInsuficienteError
from gerencia import Gerencia



class Deposito:
    def __init__(self,remesas, materiales):
        self.remesas = remesas
        self.materiales = materiales

        
    
    def generar_retiro(): #esto llama a un metodo del gestor
        return 
    
    def almacenar_remesa(self, id_remesa, id_material, id_proveedor, cantidad_recibida,
                          fecha_recepcion, fecha_vencimiento, precio_unitario):
        # Falta validar: id_remesa duplicado (IdentificadorDuplicadoError)
        # Falta validar: material existente (MaterialNoEncontradoError)
        # Falta validar: proveedor existente (ProveedorNoEncontradoError)
        return
    def modificar_materiales(self,material,id_material):
        self.material[id_material]=material

        return
    def obtener_remesas(self,remesas): #lo veo medio inecesario a esto
        return remesas
    
    def validar_reposicion(self,id_material):
        return