from exceptions import IdentificadorDeRemesaInvalidoError, IdentificadorDeRemesaDuplicadoError, MaterialNoIndicadoError, IdentificadorDeProveedorInvalidoError, RenglonDePedidoNoIndicadoError, CantidadRecibidaNoPositivaError, PrecioUnitarioNoPositivoError, CantidadAConsumirNoPositivaError, FormatoDeFechaInvalidoError, FechaDeRecepcionFuturaError, FechaDeVencimientoAnteriorALaRecepcionError, FechaDeVencimientoPasadaError, SaldoDeRemesaInsuficienteError
from validaciones import Validaciones
from datetime import date, datetime

class Remesa:
    lista_id=[]
    def __init__(self, id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, precio_unitario, fecha_recepcion, **datos_opcionales):
        Remesa.validar_id(id_remesa)
        Remesa.validar_material(material)

        if not Validaciones.es_identificador_valido(id_proveedor):
            raise IdentificadorDeProveedorInvalidoError(f"Toda remesa tiene que indicar qué proveedor la entregó con un identificador entero positivo; se recibió {id_proveedor!r}.")

        if not Validaciones.es_identificador_valido(id_renglon_pedido):
            raise RenglonDePedidoNoIndicadoError(f"Para conservar la trazabilidad, la remesa tiene que indicar de qué renglón de pedido proviene; se recibió {id_renglon_pedido!r}.")

        Remesa.validar_cantidad_recibida(cantidad_recibida)
        Remesa.validar_precio_unitario(precio_unitario)

        fecha_vencimiento = datos_opcionales.get("fecha_vencimiento")
        Remesa.validar_fecha_recepcion(fecha_recepcion)
        Remesa.validar_fecha_vencimiento(fecha_vencimiento, fecha_recepcion)

        self.id_remesa = id_remesa
        self.material = material
        self.id_proveedor = id_proveedor
        self.cantidad_recibida = cantidad_recibida
        self.saldo_disponible = cantidad_recibida
        self.precio_unitario = precio_unitario
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        self.datos_opcionales = dict(datos_opcionales)

        self.id_renglon_pedido = id_renglon_pedido

    @staticmethod
    def validar_id(id_remesa):
        if not Validaciones.es_identificador_valido(id_remesa):
            raise IdentificadorDeRemesaInvalidoError(f"El identificador de la remesa debe ser un número entero positivo; se recibió {id_remesa!r}.")
        if not Validaciones.validarid(Remesa.lista_id, id_remesa):
            raise IdentificadorDeRemesaDuplicadoError(f"Ya se registró una remesa con el identificador {id_remesa!r}.")

    @staticmethod
    def validar_material(material):
        if not Validaciones.es_texto_no_vacio(material):
            raise MaterialNoIndicadoError(f"Toda remesa tiene que indicar como texto qué material contiene; se recibió {material!r}.")

    @staticmethod
    def validar_cantidad_recibida(cantidad_recibida):
        if not Validaciones.es_positivo(cantidad_recibida):
            raise CantidadRecibidaNoPositivaError(f"La cantidad recibida en una remesa debe ser mayor que cero (RN9); se recibió {cantidad_recibida!r}.")

    @staticmethod
    def validar_precio_unitario(precio_unitario):
        if not Validaciones.es_positivo(precio_unitario):
            raise PrecioUnitarioNoPositivoError(f"El precio unitario informado por el proveedor debe ser mayor que cero; se recibió {precio_unitario!r}.")

    @staticmethod
    def validar_fecha_recepcion(fecha_recepcion):
        if not Validaciones.es_fecha(fecha_recepcion):
            raise FormatoDeFechaInvalidoError(f"La fecha de recepción debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha_recepcion!r}.")
        if Remesa._a_fecha(fecha_recepcion) > date.today():
            raise FechaDeRecepcionFuturaError(f"La fecha de recepción {fecha_recepcion} es posterior a hoy; no se puede registrar mercadería que todavía no llegó.")

    @staticmethod
    def validar_vencimiento_no_pasado(fecha_vencimiento):
        """Al ingresar mercaderia no se acepta una remesa que ya llega vencida (vencer hoy todavia es valido)."""
        if fecha_vencimiento is None:
            return
        if not Validaciones.es_fecha(fecha_vencimiento):
            raise FormatoDeFechaInvalidoError(f"La fecha de vencimiento debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha_vencimiento!r}.")
        if Remesa._a_fecha(fecha_vencimiento) < date.today():
            raise FechaDeVencimientoPasadaError(
                f"La fecha de vencimiento {fecha_vencimiento.strip()} ya pasó (hoy es {date.today().strftime('%d/%m/%Y')}); no se puede ingresar mercadería vencida."
            )

    @staticmethod
    def validar_fecha_vencimiento(fecha_vencimiento, fecha_recepcion):
        if fecha_vencimiento is None:
            return
        if not Validaciones.es_fecha(fecha_vencimiento):
            raise FormatoDeFechaInvalidoError(f"La fecha de vencimiento debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha_vencimiento!r}.")
        if Remesa._a_fecha(fecha_vencimiento) < Remesa._a_fecha(fecha_recepcion):
            raise FechaDeVencimientoAnteriorALaRecepcionError(
                f"La remesa vencería el {fecha_vencimiento}, antes de haberse recibido el {fecha_recepcion}; el vencimiento no puede ser anterior a la recepción."
            )

    @classmethod
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
    
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id

    @staticmethod
    def _a_fecha(valor):
        if isinstance(valor, str):
            return datetime.strptime(valor.strip(), "%d/%m/%Y").date()
        if isinstance(valor, datetime):
            return valor.date()
        return valor

    def obtener_dato(self, clave):
        return self.datos_opcionales.get(clave)
    def obtener_saldo(self):
        return self.saldo_disponible
    
    def obtener_id_remesa(self):
        return self.id_remesa
    
    def obtener_id_proveedor(self):
        return self.id_proveedor

    def obtener_fecha_vencimiento(self):
        return self.fecha_vencimiento
    
    def obtener_id_renglon_pedido(self):
        return self.id_renglon_pedido
    
    def obtener_material(self):
        return self.material

    def obtener_cantidad_recibida(self):
        return self.cantidad_recibida

    def obtener_precio_unitario(self):
        return self.precio_unitario

    def costo_total(self):
        return self.cantidad_recibida * self.precio_unitario
    
    @staticmethod
    def _verificar_que_la_fecha_de_consulta_sea_valida(fecha):
        if isinstance(fecha, date):
            return
        if not Validaciones.es_fecha(fecha):
            raise FormatoDeFechaInvalidoError(f"La fecha de consulta debe ser un texto dd/mm/aaaa o una fecha de Python; se recibió {fecha!r}.")

    def esta_vencida(self, fecha):
        Remesa._verificar_que_la_fecha_de_consulta_sea_valida(fecha)
        if self.fecha_vencimiento is None:
            return False
        return Remesa._a_fecha(self.fecha_vencimiento) < Remesa._a_fecha(fecha)

    def fue_recibida_para(self, fecha):
        Remesa._verificar_que_la_fecha_de_consulta_sea_valida(fecha)
        return Remesa._a_fecha(self.fecha_recepcion) <= Remesa._a_fecha(fecha)

    def es_utilizable(self, fecha):
        Remesa._verificar_que_la_fecha_de_consulta_sea_valida(fecha)
        return (self.saldo_disponible > 0
                and self.fue_recibida_para(fecha)
                and not self.esta_vencida(fecha))

    def consumir(self, cantidad):
        if not Validaciones.es_positivo(cantidad):
            raise CantidadAConsumirNoPositivaError(f"La cantidad a consumir de una remesa debe ser mayor que cero; se recibió {cantidad!r}.")
        if cantidad > self.saldo_disponible:
            raise SaldoDeRemesaInsuficienteError(
                f"La remesa {self.id_remesa!r} no tiene saldo suficiente: "
                f"se quieren consumir {cantidad} y solo quedan {self.saldo_disponible}."
            )
        self.saldo_disponible -= cantidad
        
    def __repr__(self):
        return (f"Remesa({self.id_remesa!r}, saldo={self.saldo_disponible}/"
                f"{self.cantidad_recibida}, vto={self.fecha_vencimiento})")

    def clave_fefo(self):
        sin_vencimiento = self.fecha_vencimiento is None

        if sin_vencimiento:
            vencimiento = date.max
        else:
            vencimiento = self._a_fecha(self.fecha_vencimiento)

        recepcion = self._a_fecha(self.fecha_recepcion)

        return (sin_vencimiento, vencimiento, recepcion, self.id_remesa)

    def obtener_fecha_recepcion(self):
        return self.fecha_recepcion


