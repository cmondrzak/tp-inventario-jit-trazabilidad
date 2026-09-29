from proveedor import Proveedor

from material import Material

from remesa import Remesa

from movimiento_retiro import Movimiento_retiro

from validaciones import Validaciones

from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError, RemesaNoEncontradaError, ExistenciaInsuficienteError
from gerencia import Gerencia




class Deposito:
    def __init__(self,remesas, materiales):
        self.remesas = remesas
        self.materiales = materiales

        

    def crear_remesa():
        return 
    
    def retirar(retiro, metodo_descarga):
        metodo_descarga(retiro)
    
    def almacenar_remesa(self,remesa):
        self.remesas[str(remesa.obtener_idremesa())] = remesa
        return
    def modificar_materiales(self,material,id_material):
        self.material[id_material]=material
        return
    def obtener_remesas(self,remesas): #lo veo medio inecesario a esto
        return remesas
    
    def validar_reposicion(self,id_material):
        return
    
    def reitrar_fefo(retiro):
        
        return