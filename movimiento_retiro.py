from movimiento import Movimiento
from gerencia import Gerencia
from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError
from exceptions import MaterialInvalidoError
from deposito import Deposito
from exceptions import CantidadInvalidaError

class Movimiento_retiro(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro,remesas_modificadas,materiales_modificacos,deposito,metodo_descarga):
        super().__init__(id_movimiento, fecha)
        if not Validaciones.validarid(Movimiento_retiro.lista_id,self.id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        self.id_movimiento = id_movimiento                         #falta validar atributos
        self.fecha = fecha
        self.renglones_retiro = renglones_retiro
        self.remesas_modificadas=remesas_modificadas
        self.materiales_modificacos=materiales_modificacos
        self.deposito=deposito
        self.metodo_descarga=metodo_descarga
        Movimiento_retiro.lista_id.append(self.id_movimiento)

    def agregar_renglon(self,material,cantidad):
        if material in self.materiales_modificados:
            raise MaterialInvalidoError("Ya existe un renglon que retira este material")
        if cantidad>Gerencia.existencia_disponible(self.deposito,material):
            raise CantidadInvalidaError("La cantidad a retirar exede la cantidad disponible en el deposito")
        else:
            r=RenglonRetiro(material,cantidad)
            self.renglones_retiro.append(r)
            self.id_materiales_modificacos.append(material)
            count=0
            for val in self.metodo_descarga(self.deposito.remesas_por_material(material)):
                if val.cantidad_recibida<=


            
    

        
        