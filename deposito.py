from proveedor import Proveedor

from material import Material

from remesa import Remesa

from movimiento_retiro import Movimiento_retiro

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
        return
    def modificar_materiales(self,material,id_material):
        self.materiales[id_material]=material
        return
    def obtener_remesas(self,remesas): #lo veo medio inecesario a esto
        return remesas
    
    def validar_reposicion(self,id_material):
        return
    
    def obtener_materiales(self):
        return self.materiales
    
    def remesas_por_material(self, material):
        lista = []
        for remesa in self.remesas.values():
            if remesa.obtener_material() == material:
                lista.append(remesa)
        return lista

    def remesas_utilizables(self, material, fecha):
        lista = []
        remesas_del_material = self.remesas_por_material(material)
        for remesa in remesas_del_material:
            if remesa.es_utilizable(fecha):
                lista.append(remesa)
        return lista

    def existencia_fisica(self, material):
        total = 0
        remesas_del_material = self.remesas_por_material(material)
        for remesa in remesas_del_material:
            total = total + remesa.obtener_saldo_disponible()
        return total

    def existencia_disponible(self, material, fecha):
        total = 0
        remesas_que_sirven = self.remesas_utilizables(material, fecha)
        for remesa in remesas_que_sirven:
            total = total + remesa.obtener_saldo_disponible()
        return total

    
    def retirar_fefo(retiro):
        return
    