from validaciones import Validaciones
from exceptions import IdentificadorDeMovimientoInvalidoError, IdentificadorDeMovimientoDuplicadoError, FormatoDeFechaInvalidoError, RemesaNoIndicadaEnElIngresoError, PedidoNoIndicadoEnElIngresoError
import validaciones
class Movimiento_ingreso:
    lista_id=[]
    def __init__(self, id_movimiento, fecha, remesa,pedido):
        Movimiento_ingreso.validar_id(id_movimiento)

        if not Validaciones.es_fecha(fecha):
            raise FormatoDeFechaInvalidoError(f"La fecha del movimiento debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha!r}.")

        if not Validaciones.es_identificador_valido(remesa):
            raise RemesaNoIndicadaEnElIngresoError("Todo movimiento de ingreso tiene que indicar qué remesa entró al depósito.")

        if not Validaciones.es_identificador_valido(pedido):
            raise PedidoNoIndicadoEnElIngresoError("Todo movimiento de ingreso tiene que indicar de qué pedido proviene la mercadería.")

        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.remesa = remesa
        self.pedido=pedido

    @staticmethod
    def validar_id(id_movimiento):
        if not Validaciones.es_identificador_valido(id_movimiento):
            raise IdentificadorDeMovimientoInvalidoError(f"El identificador del movimiento debe ser un número entero positivo; se recibió {id_movimiento!r}.")
        if not Validaciones.validarid(Movimiento_ingreso.lista_id,id_movimiento):
            raise IdentificadorDeMovimientoDuplicadoError(f"Ya se registró un movimiento de ingreso con el identificador {id_movimiento!r}.")

    @classmethod
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id

    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id
    
    def __repr__(self):
        return f'id = {self.id_movimiento}, fecha = {self.fecha}, remesa = {self.remesa}, pedido = {self.pedido}'
    
    def obtener_id_movimiento(self):
        return self.id_movimiento

    def obtener_fecha(self):
        return self.fecha

    def obtener_id_remesa(self):
        return self.remesa

    def obtener_id_pedido(self):
        return self.pedido

        
