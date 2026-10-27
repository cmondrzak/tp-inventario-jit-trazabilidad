from movimiento import Movimiento
from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError
from exceptions import MaterialInvalidoError
from exceptions import CantidadInvalidaError
from exceptions import EstadoInvalidoError
from deposito import Deposito


class Movimiento_retiro(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro,remesas_modificadas,materiales_modificacos,deposito,metodo_descarga,estado="no retirado"):
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
        self.estado=estado
        Movimiento_retiro.lista_id.append(self.id_movimiento)
        
    def cambiar_estado(self): #falta hacer toda la resta de las remesas, o en gestor cuando llama a esta funcion o aca.
        self.estado="retirado"
        for tup in self.remesas_modificadas:
            if tup[0].saldo_disponible()-tup[1]>=0: #ver si esta bien porque estoy modificando un elemento adentro de una tupla
                tup[0].saldo_disponible=-tup[1]
            else:
                raise CantidadInvalidaError("Se esta tratando de retirar de la remesa una cantidad que esta no posee")

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
        
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id


    def agregar_renglon(self,material,cantidad):
        remesas_posibles=self.deposito.remesas_por_material(material)
        tot=0
        for val in remesas_posibles:
            tot+=val.cantidad_recibida
        if tot<cantidad:
            raise CantidadInvalidaError

        if self.estado!="no retirado":
            raise EstadoInvalidoError
        if material in self.materiales_modificados:
            raise MaterialInvalidoError("Ya existe un renglon que retira este material")
        else:
            r=RenglonRetiro(material,cantidad)
            self.renglones_retiro.append(r)
            self.id_materiales_modificacos.append(material)
            count=cantidad
            for val in self.metodo_descarga(self.deposito.remesas_por_material(material)):
                if val.saldo_disponible<count:
                    count-=val.cantidad_recibida
                    self.remesas_modificadas.append((val,val.saldo_disponible))
                else:
                    self.remesas_modificadas.append((val,count))
            
                    


            
    

        
        