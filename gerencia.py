import datetime
from proveedor import Proveedor
from pedido import Pedido
from material import Material
from deposito import Deposito
from movimiento_retiro import Movimiento_retiro
from movimiento_ingreso import Movimiento_ingreso
from validaciones import Validaciones
from remesa import Remesa
from renglon_pedido import Renglon_pedido
from exceptions import ProveedorNoRegistradoError, MaterialNoRegistradoError, MaterialNoIndicadoError, NombreDeMaterialDuplicadoError, IdentificadorDeMovimientoDuplicadoError, MaterialRecibidoDistintoDelPedidoError, RenglonDePedidoPendienteNoEncontradoError
class Gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos_de_ingreso,movimientos_de_egreso):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos_de_ingreso = movimientos_de_ingreso
        self.movimientos_de_egreso = movimientos_de_egreso

    def material_registrado(self,nombre):
        nombre = Validaciones.normalizar_texto(nombre)
        for material in self.deposito[0].obtener_materiales().values():
            if Validaciones.normalizar_texto(material.obtener_nombre()) == nombre:
                return True
        return False

    def liberar_ids_renglones(self,renglones):
        # Si no llego una lista de renglones no hay ids que liberar (el error lo da Pedido)
        if not isinstance(renglones, list):
            return
        for renglon in renglones:
            if not isinstance(renglon, Renglon_pedido):
                continue
            if renglon.obtener_id_renglon_pedido() in Renglon_pedido.obtener_lista_id():
                Renglon_pedido.obtener_lista_id().remove(renglon.obtener_id_renglon_pedido())

    def registrar_material(self,id_material,nombre,unidad_medida,reposicion):
        # Si el nombre no es texto, el error lo da Material al validarlo
        if isinstance(nombre, str) and self.material_registrado(nombre):
            raise NombreDeMaterialDuplicadoError(f"Ya hay un material registrado con el nombre '{nombre.strip()}'; cada material debe tener un nombre único.")
        m=Material(id_material,nombre,unidad_medida,reposicion)
        self.deposito[0].modificar_materiales(m,id_material)

    def crear_deposito(self,remesas,materiales):
         d=Deposito(remesas,materiales)
         self.deposito.append(d)

    @staticmethod
    def existencia_fisica(deposito,material):
         rem = deposito.obtener_remesas()
         cantidad_total=0
         for clave,valor in rem.items():
              if valor.obtener_material()==material:
                   cantidad_total+=valor.obtener_saldo()
         return cantidad_total
        
    def registrar_proveedor(self, id_proveedor, nombre, plazo_entrega , mail,telefono):
            p = Proveedor(id_proveedor, nombre,plazo_entrega,mail = mail,telefono = telefono)
            self.proveedores[id_proveedor]=p

    @staticmethod
    def existencia_disponible(deposito,material):
         cantidad_total=0
         for remesa in deposito.remesas.values():
              if remesa.obtener_material()==material and remesa.es_utilizable(datetime.date.today()):
                   cantidad_total+=remesa.saldo_disponible
         return cantidad_total
        
    def generar_pedido(self,id_pedido,proveedor,renglones,plazo_entrega): #por ahi estaria bueno que estado pedido y renglones tengan valor por defecto al iniciar el pedido
        try:
            if proveedor not in self.proveedores:
                raise ProveedorNoRegistradoError(f"No se puede generar el pedido: no existe ningún proveedor registrado con el identificador {proveedor!r}.")
            # Si renglones no es una lista de Renglon_pedido, el error lo da Pedido al validarlos
            if isinstance(renglones, list):
                for renglon in renglones:
                    if isinstance(renglon, Renglon_pedido) and not self.material_registrado(renglon.obtener_material()):
                        raise MaterialNoRegistradoError(f"No se puede pedir '{renglon.obtener_material()}' porque ese material todavía no fue registrado en el depósito.")
            p=Pedido(id_pedido,proveedor,renglones,plazo_entrega,"Solicitado")
        except Exception:
            self.liberar_ids_renglones(renglones)
            raise
        self.pedidos[id_pedido] = p
        self.proveedores[proveedor].agregar_pedido_pendiente(p)

    def generar_retiro(self, id_movimiento, fecha, deposito):
        retiro = Movimiento_retiro(
            id_movimiento,
            fecha,
            [],
            [],
            [],
            deposito,
            deposito.retirar_fefo
        )

        self.movimientos_de_egreso[id_movimiento] = retiro
        
    def realizar_retiro(self,retiro):
         retiro.cambiar_estado()

    def obtener_pedidos(self):
        return self.pedidos
    
    def obtener_proveedores(self):
        return self.proveedores
    
    def obtener_movimientos_de_ingreso(self):
        return self.movimientos_de_ingreso
    
    def obtener_movimientos_de_egreso(self):
        return self.movimientos_de_egreso
    
    def obtener_deposito(self):
        return self.deposito
    
    def guardar_deposito(self,deposito):
        self.deposito = deposito
    
    def guardar_pedidos(self,pedidos):
        self.pedidos = pedidos
    
    def guardar_proveedores(self,proveedores):
        self.proveedores = proveedores
    
    def guardar_movimientos_de_ingreso(self,movimientos_de_ingreso):
        self.movimientos_de_ingreso = movimientos_de_ingreso

    def guardar_movimientos_de_egreso(self,movimientos_de_egreso):
        self.movimientos_de_egreso = movimientos_de_egreso
    
    
    def almacenar_remesa(self,id_movimiento_ingreso, id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales):
        if id_proveedor not in self.proveedores:
            raise ProveedorNoRegistradoError(f"No se puede registrar el ingreso: no existe ningún proveedor registrado con el identificador {id_proveedor!r}.")
        if not isinstance(material, str) or not Validaciones.es_no_vacio(material):
            raise MaterialNoIndicadoError(f"El ingreso tiene que indicar el nombre del material recibido; se recibió {material!r}.")
        material = Validaciones.normalizar_texto(material)
        if not self.material_registrado(material):
            raise MaterialNoRegistradoError(f"No se puede ingresar '{material}' porque ese material todavía no fue registrado en el depósito.")
        if not Validaciones.validarid(Movimiento_ingreso.obtener_lista_id(), id_movimiento_ingreso):
            raise IdentificadorDeMovimientoDuplicadoError(f"Ya se registró un movimiento de ingreso con el identificador {id_movimiento_ingreso!r}.")
        for pedido in self.proveedores[id_proveedor].obtener_pedidos_pendientes():
            for renglon in pedido.obtener_renglones():
                if not renglon.obtener_ingresado() and id_renglon_pedido == renglon.obtener_id_renglon_pedido() and material == Validaciones.normalizar_texto(renglon.obtener_material()) and cantidad_recibida == renglon.obtener_cantidad():
                    r = Proveedor.generar_remesa(id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales)
                    m = Movimiento_ingreso(id_movimiento_ingreso, fecha_recepcion, id_remesa, pedido.obtener_id_pedido())
                    self.movimientos_de_ingreso[id_movimiento_ingreso] = m
                    self.deposito[0].almacenar_remesa(r)
                    renglon.modificar_ingresado()
                    if all(r_pedido.obtener_ingresado() for r_pedido in pedido.obtener_renglones()):
                        self.proveedores[id_proveedor].eliminar_pedido_pendiente(pedido.obtener_id_pedido())
                    return
        # No hubo un renglon que coincida en todo: se busca el renglon por id para explicar por que
        for pedido in self.proveedores[id_proveedor].obtener_pedidos_pendientes():
            for renglon in pedido.obtener_renglones():
                if id_renglon_pedido == renglon.obtener_id_renglon_pedido() and not renglon.obtener_ingresado():
                    if material != Validaciones.normalizar_texto(renglon.obtener_material()):
                        raise MaterialRecibidoDistintoDelPedidoError(f"Se recibió '{material}', pero el renglón {id_renglon_pedido!r} del pedido solicitaba '{renglon.obtener_material()}'.")
                    raise RenglonDePedidoPendienteNoEncontradoError(f"El renglón {id_renglon_pedido!r} del pedido solicitaba {renglon.obtener_cantidad()}, pero se recibieron {cantidad_recibida}; la cantidad recibida tiene que coincidir con la pedida.")
        raise RenglonDePedidoPendienteNoEncontradoError(f"El proveedor {id_proveedor!r} no tiene ningún pedido pendiente con el renglón {id_renglon_pedido!r} sin ingresar.")
