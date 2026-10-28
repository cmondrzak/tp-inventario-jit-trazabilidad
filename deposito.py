from datetime import date

from proveedor import Proveedor

from material import Material

from remesa import Remesa

from validaciones import Validaciones

from exceptions import CantidadInvalidaError, PrecioInvalidoError, SaldoInvalidoError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError, RemesaNoEncontradaError, ExistenciaInsuficienteError





class Deposito:
    def __init__(self,remesas, materiales):
        self.remesas = remesas
        self.materiales = materiales
    
    # def retirar(retiro, metodo_descarga):
    #     metodo_descarga(retiro)
    
    def almacenar_remesa(self,remesa):
        self.remesas[str(remesa.obtener_id_remesa())] = remesa

    def modificar_materiales(self,material,id_material):
        self.materiales[id_material]=material
        return
    def obtener_remesas(self):
        return self.remesas
    
    def validar_reposicion(self,id_material):
        return
    
    def obtener_materiales(self):
        return self.materiales.copy()
    
    def remesas_por_material(self, material):
        lista = []
        for remesa in self.remesas.values():
            if remesa.obtener_material() == material and not remesa.esta_vencida(date.today()) and remesa.obtener_saldo()>0:
                lista.append(remesa)
        return lista


    
    def retirar_fefo(retiro):
        return
    