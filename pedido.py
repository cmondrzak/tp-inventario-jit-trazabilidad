from validaciones import Validaciones
from exceptions import IdentificadorDePedidoInvalidoError, IdentificadorDePedidoDuplicadoError, ProveedorNoIndicadoError, PlazoDeEntregaNoPositivoError, RenglonesDelPedidoNoSonUnaListaError, PedidoSinRenglonesError, ElementoNoEsUnRenglonDePedidoError, MaterialRepetidoEnElPedidoError, IdentificadorDeRenglonDePedidoDuplicadoError, EstadoDePedidoInvalidoError, FormatoDeFechaInvalidoError, FechaDeRecepcionAnteriorAlPedidoError
from renglon_pedido import Renglon_pedido
from lista_enlazada import ListaEnlazada
from datetime import date, datetime

class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega):
        Pedido.validar_id(id_pedido)

        if not Validaciones.es_identificador_valido(proveedor):
            raise ProveedorNoIndicadoError("Todo pedido tiene que estar dirigido a un proveedor (RN29), pero no se indicó ninguno.")

        Pedido.validar_plazo_entrega(plazo_entrega)

        if not isinstance(renglones, list):
            raise RenglonesDelPedidoNoSonUnaListaError(f"Los renglones del pedido tienen que venir en una lista, pero se recibió un objeto de tipo {type(renglones).__name__}.")

        if len(renglones) == 0:
            raise PedidoSinRenglonesError("Un pedido tiene que incluir al menos un renglón (RN30), pero la lista recibida está vacía.")

        for renglon in renglones:
            if not isinstance(renglon, Renglon_pedido):
                raise ElementoNoEsUnRenglonDePedidoError(f"Todos los elementos de la lista tienen que ser renglones de pedido, pero se encontró un objeto de tipo {type(renglon).__name__}.")

        renglones_revisados = []
        for renglon in renglones:
            Pedido.validar_id_renglon_nuevo(renglones_revisados, renglon.obtener_id_renglon_pedido())
            Pedido.validar_material_renglon_nuevo(renglones_revisados, renglon.obtener_material())
            renglones_revisados.append(renglon)

        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self._renglones = ListaEnlazada()

        for renglon in renglones:
            self._renglones.agregar_final(renglon)

        self.plazo_entrega=plazo_entrega
        self.estado = "Solicitado"
        self.fecha_solicitud = date.today()
        self.fecha_inicio_espera = self.fecha_solicitud
        self.motivo_rechazo = None

    @staticmethod
    def validar_id(id_pedido):
        if not Validaciones.es_identificador_valido(id_pedido):
            raise IdentificadorDePedidoInvalidoError(f"El identificador del pedido debe ser un número entero positivo; se recibió {id_pedido!r}.")
        if not Validaciones.validarid(Pedido.lista_id,id_pedido):
            raise IdentificadorDePedidoDuplicadoError(f"Ya existe un pedido con el identificador {id_pedido!r}.")

    @staticmethod
    def validar_plazo_entrega(plazo_entrega):
        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoDeEntregaNoPositivoError(f"El plazo de entrega del pedido debe ser de al menos un día; se recibió {plazo_entrega!r}.")

    @staticmethod
    def validar_id_renglon_nuevo(renglones, id_renglon):
        for renglon in renglones:
            if renglon.obtener_id_renglon_pedido() == id_renglon:
                raise IdentificadorDeRenglonDePedidoDuplicadoError(f"El identificador de renglón {id_renglon!r} ya se usó en otro renglón de este pedido.")

    @staticmethod
    def validar_material_renglon_nuevo(renglones, material):
        if Pedido.tiene_renglon_con_material(renglones, material):
            raise MaterialRepetidoEnElPedidoError(f"El material '{material}' ya está en otro renglón; cada material se pide en un único renglón.")

    @classmethod
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

    def registrar_ids(self):
        Pedido.registrar_id(self.id_pedido)
        for renglon in self.obtener_renglones():
            Renglon_pedido.registrar_id(renglon.obtener_id_renglon_pedido())

    @classmethod
    def guardar_lista_id(cls,lista_id):
        cls.lista_id = lista_id
    
    @classmethod
    def obtener_lista_id(cls):
        return cls.lista_id
    
    def obtener_renglones(self):
        return self._renglones.obtener_datos()
    
    def obtener_id_pedido(self):
        return self.id_pedido
    
    def __repr__(self):
        return f'{self.id_pedido},{self.proveedor},{self.obtener_renglones()},{self.plazo_entrega},{self.estado}'

    @staticmethod
    def tiene_renglon_con_material(renglones, material):
        def normalizar(valor):
            return Validaciones.normalizar_texto(valor) if isinstance(valor, str) else valor
        buscado = normalizar(material)
        for renglon in renglones:
            if normalizar(renglon.obtener_material()) == buscado:
                return True
        return False

    def generar_renglon(self,id_renglon,material,cantidad,precio_unitario):
        self.validar_edicion()
        if Pedido.tiene_renglon_con_material(self.obtener_renglones(), material):
            raise MaterialRepetidoEnElPedidoError(f"El pedido {self.id_pedido!r} ya tiene un renglón para '{material}'; no se puede agregar un segundo renglón del mismo material.")
        renglon = Renglon_pedido(id_renglon,material,cantidad,precio_unitario)
        self._renglones.agregar_final(renglon)
        Renglon_pedido.registrar_id(id_renglon)

    def subtotal(self):
        sub_total=0

        for renglon in self.obtener_renglones():
            sub_total+=renglon.subtotal_renglon()
        return sub_total
    
    def eliminar_renglon_pedido(self,id_renglon):
        self.validar_edicion()
        renglones = self.obtener_renglones()

        for renglon in renglones:
            if renglon.obtener_id_renglon_pedido()==id_renglon:
                if len(renglones)==1:
                    raise PedidoSinRenglonesError(
                        "No se puede eliminar el unico renglon del pedido."
                    )

                self._renglones.eliminar(renglon)
                return

        raise ValueError("No existe un renglon con ese ID.")
    
    def obtener_estado(self):
        return self.estado

    def obtener_id_proveedor(self):
        return self.proveedor

    def obtener_fecha_solicitud(self):
        return self.fecha_solicitud

    def obtener_motivo_rechazo(self):
        return self.motivo_rechazo

    def actualizar_vencimiento(self):
        if self.estado=="Solicitado":
            dias = (date.today()-self.fecha_inicio_espera).days

            if dias>=30:
                self.estado = "Rechazado"
                self.motivo_rechazo = (
                    "Pasaron 30 dias sin aceptacion del proveedor."
                )

    def aceptar(self):
        self.actualizar_vencimiento()

        if self.estado!="Solicitado":
            raise EstadoDePedidoInvalidoError(
                f"No se puede aceptar un pedido en estado '{self.estado}'."
            )

        self.estado = "Aceptado"

    def rechazar(self,motivo):
        self.actualizar_vencimiento()

        if self.estado!="Solicitado":
            raise EstadoDePedidoInvalidoError(
                f"No se puede rechazar un pedido en estado '{self.estado}'."
            )

        if not isinstance(motivo,str) or not motivo.strip():
            raise EstadoDePedidoInvalidoError(
                "Debe indicar el motivo del rechazo."
            )

        self.estado = "Rechazado"
        self.motivo_rechazo = motivo.strip()

    def validar_recepcion(self):
        self.actualizar_vencimiento()

        if self.estado not in ["Aceptado","En proceso"]:
            raise EstadoDePedidoInvalidoError(
                f"No se pueden recibir materiales de un pedido "
                f"en estado '{self.estado}'."
            )

    def validar_fecha_recepcion(self, fecha_recepcion):
        if not Validaciones.es_fecha(fecha_recepcion):
            raise FormatoDeFechaInvalidoError(f"La fecha de recepción debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha_recepcion!r}.")

        recepcion = datetime.strptime(fecha_recepcion.strip(), "%d/%m/%Y").date()
        if recepcion < self.fecha_solicitud:
            raise FechaDeRecepcionAnteriorAlPedidoError(
                f"La remesa se habría recibido el {fecha_recepcion}, antes de que se hiciera el pedido "
                f"{self.id_pedido} ({self.fecha_solicitud.strftime('%d/%m/%Y')})."
            )

    def actualizar_estado_recepcion(self):
        self.validar_recepcion()

        ingresados = 0
        renglones = self.obtener_renglones()

        for renglon in renglones:
            if renglon.obtener_ingresado():
                ingresados += 1

        if ingresados==len(renglones):
            self.estado = "Recibido"
        elif ingresados>0:
            self.estado = "En proceso"

    def validar_edicion(self):
        self.actualizar_vencimiento()

        if self.estado!="Solicitado":
            raise EstadoDePedidoInvalidoError(
                "Solo se pueden editar pedidos solicitados."
            )