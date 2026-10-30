from validaciones import Validaciones
from exceptions import IdentificadorDePedidoInvalidoError, IdentificadorDePedidoDuplicadoError, ProveedorNoIndicadoError, PlazoDeEntregaNoPositivoError, RenglonesDelPedidoNoSonUnaListaError, PedidoSinRenglonesError, ElementoNoEsUnRenglonDePedidoError, MaterialRepetidoEnElPedidoError, EstadoDePedidoInvalidoError
from renglon_pedido import Renglon_pedido
from lista_enlazada import ListaEnlazada

class Pedido:
    lista_id=[]
    def __init__(self, id_pedido, proveedor, renglones,plazo_entrega,estado):

        if not Validaciones.es_identificador_valido(id_pedido):
            raise IdentificadorDePedidoInvalidoError(f"El identificador del pedido debe ser un número entero positivo o un texto con contenido; se recibió {id_pedido!r}.")

        if not Validaciones.validarid(Pedido.lista_id,id_pedido):
            raise IdentificadorDePedidoDuplicadoError(f"Ya existe un pedido con el identificador {id_pedido!r}.")

        if not Validaciones.es_identificador_valido(proveedor):
            raise ProveedorNoIndicadoError("Todo pedido tiene que estar dirigido a un proveedor (RN29), pero no se indicó ninguno.")

        if not Validaciones.es_positivo(plazo_entrega):
            raise PlazoDeEntregaNoPositivoError(f"El plazo de entrega del pedido debe ser de al menos un día; se recibió {plazo_entrega!r}.")

        if not isinstance(renglones, list):
            raise RenglonesDelPedidoNoSonUnaListaError(f"Los renglones del pedido tienen que venir en una lista, pero se recibió un objeto de tipo {type(renglones).__name__}.")

        if len(renglones) == 0:
            raise PedidoSinRenglonesError("Un pedido tiene que incluir al menos un renglón (RN30), pero la lista recibida está vacía.")

        for renglon in renglones:
            if not isinstance(renglon, Renglon_pedido):
                raise ElementoNoEsUnRenglonDePedidoError(f"Todos los elementos de la lista tienen que ser renglones de pedido, pero se encontró un objeto de tipo {type(renglon).__name__}.")

        renglones_revisados = []
        for renglon in renglones:
            if Pedido.tiene_renglon_con_material(renglones_revisados, renglon.obtener_material()):
                raise MaterialRepetidoEnElPedidoError(f"El material '{renglon.obtener_material()}' aparece en más de un renglón; cada material se pide en un único renglón.")
            renglones_revisados.append(renglon)

        self.id_pedido = id_pedido
        self.proveedor = proveedor
        self._renglones = ListaEnlazada()

        for renglon in renglones:
            self._renglones.agregar_final(renglon)

        self.plazo_entrega=plazo_entrega
        self.estado=estado
        Pedido.lista_id.append(self.id_pedido)

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
        if Pedido.tiene_renglon_con_material(self.obtener_renglones(), material):
            raise MaterialRepetidoEnElPedidoError(f"El pedido {self.id_pedido!r} ya tiene un renglón para '{material}'; no se puede agregar un segundo renglón del mismo material.")
        renglon = Renglon_pedido(id_renglon,material,cantidad,precio_unitario)
        self._renglones.agregar_final(renglon)

    def subtotal(self):
        sub_total=0

        for renglon in self.obtener_renglones():
            sub_total+=renglon.subtotal_renglon()
        return sub_total
    
    def eliminar_renglon_pedido(self,id_renglon):
        for renglon in self.obtener_renglones():
            if renglon.obtener_id_renglon_pedido() == id_renglon:
                self._renglones.eliminar(renglon)
                return

        raise ValueError("No existe un renglon con ese ID en el pedido.")
    
    def cambiar_estado(self,nuevo_estado):
        estados_validos = ["Pendiente", "En Proceso", "Completado"]

        if nuevo_estado not in estados_validos:
            raise EstadoDePedidoInvalidoError(f"El estado {nuevo_estado!r} no es válido. Debe ser 'Pendiente', 'En Proceso' o 'Completado'.")

        self.estado=nuevo_estado