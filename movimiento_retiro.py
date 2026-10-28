from movimiento import Movimiento
from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError
from exceptions import MaterialInvalidoError
from exceptions import CantidadInvalidaError
from exceptions import EstadoInvalidoError
from deposito import Deposito
from remesa import Remesa


class Movimiento_retiro(Movimiento):
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro,remesas_modificadas,materiales_modificacos,deposito,metodo_descarga,estado="no retirado"):
        super().__init__(fecha)
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

    def eliminar_renglon(self,material):
        if self.estado!="no retirado":
            raise EstadoInvalidoError("El retiro ya fue realizado")

        for renglon in self.renglones_retiro:
            if renglon.material==material:
                remesas_restantes=[]
                for tup in self.remesas_modificadas:
                    if tup[0].obtener_material()!=material:
                        remesas_restantes.append(tup)

                if material in self.materiales_modificacos:
                    self.materiales_modificacos.remove(material)

                self.renglones_retiro.remove(renglon)
                self.remesas_modificadas=remesas_restantes
                return

        raise MaterialInvalidoError("No existe un renglon con ese material")
        



        
    def cambiar_estado(self):
        if self.estado!='no retirado':
            raise EstadoInvalidoError
        for tup in self.remesas_modificadas:
            tup[0].consumir(tup[1])
        self.estado="retirado"

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
            tot+=val.obtener_saldo_disponible()
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
                    count-=val.saldo_disponible
                    self.remesas_modificadas.append((val,val.saldo_disponible))
                else:
                    self.remesas_modificadas.append((val,count))
                    break
                    
            
                    


            
    

        
        