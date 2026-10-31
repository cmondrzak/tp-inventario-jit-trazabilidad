from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDeMovimientoInvalidoError
from exceptions import IdentificadorDeMovimientoDuplicadoError
from exceptions import FormatoDeFechaInvalidoError
from exceptions import MaterialInvalidoError
from exceptions import MaterialRepetidoEnElRetiroError
from exceptions import CantidadARetirarNoPositivaError
from exceptions import ExistenciaDisponibleInsuficienteParaElRetiroError
from exceptions import RetiroYaRealizadoError
from exceptions import EstadoInvalidoError
from deposito import Deposito
from remesa import Remesa


class Movimiento_retiro:
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro,remesas_modificadas,materiales_modificados,deposito,metodo_descarga,estado="no retirado"):
        if not Validaciones.es_identificador_valido(id_movimiento):
            raise IdentificadorDeMovimientoInvalidoError(f"El identificador del movimiento debe ser un número entero positivo o un texto con contenido; se recibió {id_movimiento!r}.")

        if not Validaciones.validarid(Movimiento_retiro.lista_id,id_movimiento):
            raise IdentificadorDeMovimientoDuplicadoError(f"Ya existe un movimiento de retiro con el identificador {id_movimiento!r}.")

        if not Validaciones.es_fecha(fecha):
            raise FormatoDeFechaInvalidoError(f"La fecha del retiro debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha!r}.")

        self.id_movimiento = id_movimiento                  
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
            raise RetiroYaRealizadoError("No se pueden quitar renglones de un retiro que ya fue realizado.")

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

        raise MaterialInvalidoError(f"El retiro no tiene ningún renglón para el material {material!r}.")
        

    def _planificar_consumo(self, material, cantidad):
        if not Validaciones.es_positivo(cantidad):
            raise CantidadARetirarNoPositivaError(
                f"La cantidad a retirar debe ser mayor que cero; se pidió {cantidad!r}."
            )

        disponibles = self.deposito.remesas_por_material(
            material,
            self.fecha
        )

        total = 0
        for remesa in disponibles:
            total += remesa.obtener_saldo()

        if total < cantidad:
            raise ExistenciaDisponibleInsuficienteParaElRetiroError(
                f"Se quieren retirar {cantidad} de '{material}', pero la existencia disponible al {self.fecha} es {total}."
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
            raise RetiroYaRealizadoError(
                "El retiro ya fue realizado; no se puede volver a confirmar."
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

        for remesa, cantidad in plan_completo:
            self.deposito.archivar_remesa_agotada(remesa)

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
            raise RetiroYaRealizadoError(
                "No se pueden agregar renglones a un retiro que ya fue realizado."
            )

        material = Validaciones.normalizar_texto(material)

        if material in self.materiales_modificados:
            raise MaterialRepetidoEnElRetiroError(
                "Este retiro ya tiene un renglón para ese material; sumá la cantidad en ese renglón en lugar de agregar otro."
            )

        renglon = RenglonRetiro(material, cantidad)
        plan = self._planificar_consumo(material, cantidad)

        self.renglones_retiro.append(renglon)
        self.materiales_modificados.append(material)

        for consumo in plan:
            self.remesas_modificadas.append(consumo)
                    
            
                    


            
    

        
        