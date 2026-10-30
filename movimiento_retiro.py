from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError
from exceptions import FechaInvalidaError
from exceptions import MaterialInvalidoError
from exceptions import CantidadInvalidaError
from exceptions import EstadoInvalidoError
from deposito import Deposito
from remesa import Remesa


class Movimiento_retiro:
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro,remesas_modificadas,materiales_modificados,deposito,metodo_descarga,estado="no retirado"):
        if not Validaciones.es_fecha(fecha):
            raise FechaInvalidaError("Fecha invalida.")

        if not Validaciones.validarid(Movimiento_retiro.lista_id,id_movimiento):
            raise IdentificadorDuplicadoError("El identificador ya existe en la lista.")

        self.id_movimiento = id_movimiento                         #falta validar atributos
        self.fecha = fecha
        self.renglones_retiro = renglones_retiro
        self.remesas_modificadas=remesas_modificadas
        self.materiales_modificados=materiales_modificados
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

                if material in self.materiales_modificados:
                    self.materiales_modificados.remove(material)

                self.renglones_retiro.remove(renglon)
                self.remesas_modificadas=remesas_restantes
                return

        raise MaterialInvalidoError("No existe un renglon con ese material")
        

    def _planificar_consumo(self, material, cantidad):
        if not Validaciones.es_positivo(cantidad):
            raise CantidadInvalidaError(
                "La cantidad debe ser mayor que cero."
            )

        disponibles = self.deposito.remesas_por_material(
            material,
            self.fecha
        )

        total = 0
        for remesa in disponibles:
            total += remesa.obtener_saldo()

        if total < cantidad:
            raise CantidadInvalidaError(
                "No hay suficiente stock disponible."
            )

        ordenadas = self.metodo_descarga(disponibles)
        #probablemente aca podria implementarse recursividad sin grandes complicaciones (linea 74 a 91)
        plan = []
        faltante = cantidad

        for remesa in ordenadas:
            saldo = remesa.obtener_saldo()

            if saldo < faltante:
                cantidad_a_retirar = saldo
            else:
                cantidad_a_retirar = faltante

            plan.append((remesa, cantidad_a_retirar))
            faltante -= cantidad_a_retirar

            if faltante == 0:
                break

        return plan

        
    def cambiar_estado(self):
        if self.estado != "no retirado":
            raise EstadoInvalidoError(
                "El retiro ya fue realizado."
            )

        if not self.renglones_retiro:
            raise EstadoInvalidoError(
                "No se puede confirmar un retiro sin renglones."
            )

        plan_completo = []
        #corregir encapsulamiento (linea 109 y 110)
        for renglon in self.renglones_retiro:
            plan = self._planificar_consumo(
                renglon.material,
                renglon.cantidad_solicitada
            )

            for consumo in plan:
                plan_completo.append(consumo)

        for remesa, cantidad in plan_completo:
            remesa.consumir(cantidad)

        self.remesas_modificadas = plan_completo
        self.estado = "retirado"

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
        
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id


    def agregar_renglon(self, material, cantidad):
        if self.estado != "no retirado":
            raise EstadoInvalidoError(
                "El retiro ya fue realizado."
            )

        material = Validaciones.normalizar_texto(material)

        if material in self.materiales_modificados:
            raise MaterialInvalidoError(
                "Ya existe un renglón para este material."
            )

        renglon = RenglonRetiro(material, cantidad)
        plan = self._planificar_consumo(material, cantidad)

        self.renglones_retiro.append(renglon)
        self.materiales_modificados.append(material)

        for consumo in plan:
            self.remesas_modificadas.append(consumo)
                    
            
                    


            
    

        
        