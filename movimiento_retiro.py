from movimiento import Movimiento
#from gerencia import Gerencia
from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError
from exceptions import MaterialInvalidoError
from exceptions import CantidadInvalidaError
from exceptions import EstadoInvalidoError

class cola:
    def __init__(self, elementos=None):
        if elementos is None:
            self.__elementos = []
        else:
            self.__elementos = list(elementos)

    def encolar(self, dato):
        self.__elementos.append(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self.__elementos.pop(0)

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self.__elementos[0]

    def esta_vacia(self):
        return len(self.__elementos) == 0

    def __len__(self):
        return len(self.__elementos)

    def __repr__(self):
        return f"cola({self.__elementos})"

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


    def agregar_renglon(self,material,cantidad):
        if self.estado!="no retirado":
            raise EstadoInvalidoError
        if material in self.materiales_modificados:
            raise MaterialInvalidoError("Ya existe un renglon que retira este material")
        #if cantidad>Gerencia.existencia_disponible(self.deposito,material):
            raise CantidadInvalidaError("La cantidad a retirar exede la cantidad disponible en el deposito")
        else:
            r=RenglonRetiro(material,cantidad)
            self.renglones_retiro.append(r)
            self.id_materiales_modificacos.append(material)
            count=cantidad
            for val in self.metodo_descarga(self.deposito.remesas_por_material(material)):
                if val.cantidad_recibida<count:
                    count-=val.cantidad_recibida
                    self.remesas_modificadas.append((val,val.cantidad_recibida))
                else:
                    self.remesas_modificadas.append(val,count)
            
                    


            
    

        
        