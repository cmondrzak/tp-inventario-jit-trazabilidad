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
from renglon_retiro import RenglonRetiro
from exceptions import ProveedorNoRegistradoError, MaterialNoRegistradoError, MaterialNoIndicadoError, NombreDeMaterialDuplicadoError, NombreDeProveedorDuplicadoError, PedidoDeOtroProveedorError, RenglonDePedidoPendienteNoEncontradoError, EntidadNoEncontradaError, EstadoInvalidoError
class Gerencia():
    def __init__(self,deposito,pedidos,proveedores,movimientos_de_ingreso,movimientos_de_egreso):
        self.deposito=deposito
        self.pedidos=pedidos
        self.proveedores=proveedores
        self.movimientos_de_ingreso = movimientos_de_ingreso
        self.movimientos_de_egreso = movimientos_de_egreso

    def material_registrado(self,nombre):
        return self.deposito[0].material_registrado(nombre)


    def validar_nombre_material_nuevo(self, nombre):
        if isinstance(nombre, str) and self.material_registrado(nombre):
            raise NombreDeMaterialDuplicadoError(f"Ya hay un material registrado con el nombre '{nombre.strip()}'; cada material debe tener un nombre único.")

    def registrar_material(self,id_material,nombre,unidad_medida,reposicion):
        self.validar_nombre_material_nuevo(nombre)
        m=Material(id_material,nombre,unidad_medida,reposicion)
        self.deposito[0].modificar_materiales(m,id_material)

    def crear_deposito(self,remesas,materiales):
         d=Deposito(remesas,materiales)
         self.deposito.append(d)

    def validar_nombre_proveedor_nuevo(self, nombre):
        if not isinstance(nombre, str):
            return
        buscado = Validaciones.normalizar_texto(nombre)
        for proveedor in self.proveedores.values():
            if Validaciones.normalizar_texto(proveedor.obtener_nombre()) == buscado:
                raise NombreDeProveedorDuplicadoError(f"Ya hay un proveedor registrado con el nombre '{proveedor.obtener_nombre()}' (id {proveedor.obtener_idproveedor()}).")

    def registrar_proveedor(self, id_proveedor, nombre, plazo_entrega, mail,telefono):
            self.validar_nombre_proveedor_nuevo(nombre)
            p = Proveedor(id_proveedor, nombre,plazo_entrega,mail = mail,telefono = telefono)
            self.proveedores[id_proveedor]=p
            Proveedor.registrar_id(id_proveedor)

    def consultar_existencia(self, material, fecha_consulta, incluir_vencidas):
        """Existencia de un material a una fecha (date): recibido hasta esa fecha menos lo retirado hasta esa fecha.

        Con incluir_vencidas=True es la existencia fisica; con False, la disponible.
        """
        total = 0
        for remesa in self.deposito[0].obtener_todas_las_remesas().values():
            if remesa.obtener_material() == material and remesa.fue_recibida_para(fecha_consulta):
                if incluir_vencidas or not remesa.esta_vencida(fecha_consulta):
                    cantidad = remesa.obtener_cantidad_recibida()
                    for retiro in self.movimientos_de_egreso.values():
                        if retiro.obtener_estado() == "retirado" and datetime.datetime.strptime(retiro.obtener_fecha().strip(), "%d/%m/%Y").date() <= fecha_consulta:
                            for remesa_retirada, cantidad_retirada in retiro.obtener_remesas_modificadas():
                                if remesa_retirada.obtener_id_remesa() == remesa.obtener_id_remesa():
                                    cantidad -= cantidad_retirada
                    total += cantidad
        return total

    def crear_borrador_pedido(self,id_pedido,proveedor,renglones):
        """Arma el pedido validado pero sin registrarlo: mientras es borrador se le pueden agregar y quitar renglones.

        El pedido toma como plazo de entrega el que tiene registrado su proveedor.
        """
        self.validar_proveedor_registrado(proveedor)
        if isinstance(renglones, list):
            for renglon in renglones:
                if isinstance(renglon, Renglon_pedido) and not self.material_registrado(renglon.obtener_material()):
                    raise MaterialNoRegistradoError(f"No se puede pedir '{renglon.obtener_material()}' porque ese material todavía no fue registrado en el depósito.")
        return Pedido(id_pedido,proveedor,renglones,self.proveedores[proveedor].obtener_plazo_entrega())

    def agregar_renglon_a_pedido(self,pedido,id_renglon,material,cantidad):
        self.validar_material_en_deposito(material)
        pedido.generar_renglon(id_renglon,material,cantidad)

    @staticmethod
    def eliminar_renglon_de_pedido(pedido,id_renglon):
        pedido.eliminar_renglon_pedido(id_renglon)

    def registrar_pedido(self,pedido):
        Pedido.validar_id(pedido.obtener_id_pedido())
        self.validar_proveedor_registrado(pedido.obtener_id_proveedor())
        self.proveedores[pedido.obtener_id_proveedor()].agregar_pedido_pendiente(pedido)
        self.pedidos[pedido.obtener_id_pedido()] = pedido
        pedido.registrar_ids()

    def crear_borrador_retiro(self, id_movimiento, fecha, renglones):
        """Arma el retiro validado pero sin registrarlo ni descontar stock: mientras es borrador se le pueden agregar y quitar renglones."""
        deposito = self.deposito[0]
        return Movimiento_retiro(id_movimiento, fecha, renglones, deposito, deposito.retirar_fefo)

    @staticmethod
    def agregar_renglon_a_retiro(retiro, material, cantidad):
        retiro.agregar_renglon(material, cantidad)

    @staticmethod
    def eliminar_renglon_de_retiro(retiro, material):
        retiro.eliminar_renglon(material)

    def registrar_retiro(self, retiro):
        """Confirma el retiro (descuenta el stock) y recien entonces lo registra."""
        Movimiento_retiro.validar_id(retiro.obtener_id_movimiento())
        retiro.cambiar_estado()
        self.movimientos_de_egreso[retiro.obtener_id_movimiento()] = retiro
        Movimiento_retiro.registrar_id(retiro.obtener_id_movimiento())

    def obtener_pedidos(self):
        return self.pedidos.copy()

    def obtener_proveedores(self):
        return self.proveedores.copy()

    def obtener_movimientos_de_ingreso(self):
        return self.movimientos_de_ingreso.copy()

    def obtener_movimientos_de_egreso(self):
        return self.movimientos_de_egreso.copy()

    def obtener_deposito(self):
        return self.deposito.copy()

    def obtener_deposito_principal(self):
        return self.deposito[0]

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
    
    
    def validar_proveedor_registrado(self, id_proveedor):
        if id_proveedor not in self.proveedores:
            raise ProveedorNoRegistradoError(f"No existe ningún proveedor registrado con el identificador {id_proveedor!r}.")

    def buscar_renglon_pendiente(self, id_proveedor, id_renglon_pedido):
        """Devuelve (pedido, renglon) del renglon sin ingresar con ese id, verificando que el pedido sea del proveedor indicado."""
        self.validar_proveedor_registrado(id_proveedor)
        self.actualizar_estados_pedidos()
        for pedido in self.pedidos.values():
            for renglon in pedido.obtener_renglones():
                if renglon.obtener_id_renglon_pedido() == id_renglon_pedido:
                    if pedido.obtener_id_proveedor() != id_proveedor:
                        raise PedidoDeOtroProveedorError(f"El renglón {id_renglon_pedido!r} pertenece al pedido {pedido.obtener_id_pedido()} del proveedor {pedido.obtener_id_proveedor()}, no del proveedor {id_proveedor}; la remesa no coincide con el pedido.")
                    if renglon.obtener_ingresado():
                        raise RenglonDePedidoPendienteNoEncontradoError(f"El renglón {id_renglon_pedido!r} del pedido {pedido.obtener_id_pedido()} ya fue recibido.")
                    pedido.validar_recepcion()
                    return pedido, renglon
        raise RenglonDePedidoPendienteNoEncontradoError(f"No existe ningún renglón de pedido con el identificador {id_renglon_pedido!r}.")

    def almacenar_remesa(self,id_movimiento_ingreso, id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, precio_unitario, fecha_recepcion, **datos_opcionales):
        Movimiento_ingreso.validar_id(id_movimiento_ingreso)
        Remesa.validar_id(id_remesa)
        Remesa.validar_material(material)
        material = Validaciones.normalizar_texto(material)
        self.deposito[0].validar_material_registrado(material)

        pedido, renglon = self.buscar_renglon_pendiente(id_proveedor, id_renglon_pedido)
        renglon.validar_material_recibido(material)
        renglon.validar_cantidad_recibida(cantidad_recibida)
        Remesa.validar_precio_unitario(precio_unitario)
        pedido.validar_fecha_recepcion(fecha_recepcion)
        Remesa.validar_vencimiento_no_pasado(datos_opcionales.get("fecha_vencimiento"))

        r = Proveedor.generar_remesa(id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, precio_unitario, fecha_recepcion, **datos_opcionales)
        m = Movimiento_ingreso(id_movimiento_ingreso, fecha_recepcion, id_remesa, pedido.obtener_id_pedido())
        self.deposito[0].almacenar_remesa(r)
        self.movimientos_de_ingreso[id_movimiento_ingreso] = m
        Movimiento_ingreso.registrar_id(id_movimiento_ingreso)
        renglon.modificar_ingresado()
        pedido.actualizar_estado_recepcion()

        if pedido.obtener_estado()=="Recibido":
            self.proveedores[id_proveedor].eliminar_pedido_pendiente(
                pedido.obtener_id_pedido()
            )
    
    def obtener_materiales_a_reponer(self):
        return self.deposito[0].obtener_materiales_a_reponer()

    def consultar_reposicion(self,nombre):
        if not isinstance(nombre,str) or not Validaciones.es_no_vacio(nombre):
            raise MaterialNoIndicadoError(
                "Debe indicar el nombre del material."
            )

        nombre = Validaciones.normalizar_texto(nombre)

        for id_material, material in self.deposito[0].obtener_materiales().items():
            if Validaciones.normalizar_texto(material.obtener_nombre())==nombre:
                return self.deposito[0].obtener_datos_reposicion(
                    id_material
                )

        raise MaterialNoRegistradoError(
            f"No existe un material registrado con el nombre '{nombre}'."
        )
    def consultar_trazabilidad_retiro(self,id_retiro):
        if id_retiro not in self.movimientos_de_egreso:
            raise EntidadNoEncontradaError(
                f"No existe un retiro con el identificador {id_retiro}."
            )

        retiro = self.movimientos_de_egreso[id_retiro]

        if retiro.obtener_estado()!="retirado":
            raise EstadoInvalidoError(
                "El retiro todavia no fue realizado; no hay consumos confirmados."
            )

        renglones = []

        for renglon in retiro.obtener_renglones():
            renglones.append({
                "material": renglon.obtener_material(),
                "cantidad": renglon.obtener_cantidad_solicitada()
            })

        remesas = []

        for remesa, cantidad in retiro.obtener_remesas_modificadas():
            remesas.append({
                "id_remesa": remesa.obtener_id_remesa(),
                "material": remesa.obtener_material(),
                "cantidad": cantidad
            })

        return {
            "id_retiro": retiro.obtener_id_movimiento(),
            "fecha": retiro.obtener_fecha(),
            "estado": retiro.obtener_estado(),
            "renglones": renglones,
            "remesas": remesas
        }
    def consultar_trazabilidad_remesa(self,id_remesa):
        try:
            remesa = self.deposito[0].obtener_remesa(id_remesa)
        except KeyError:
            raise EntidadNoEncontradaError(
                f"No existe una remesa con el identificador {id_remesa}."
            )

        ingreso_encontrado = None

        for ingreso in self.movimientos_de_ingreso.values():
            if str(ingreso.obtener_id_remesa())==str(id_remesa):
                ingreso_encontrado = ingreso
                break

        if ingreso_encontrado is None:
            raise EntidadNoEncontradaError(
                "La remesa existe, pero no se encontro su movimiento de ingreso."
            )

        retiros = []

        for retiro in self.movimientos_de_egreso.values():
            if retiro.obtener_estado()!="retirado":
                continue

            for remesa_consumida, cantidad in retiro.obtener_remesas_modificadas():
                if str(remesa_consumida.obtener_id_remesa())==str(id_remesa):
                    retiros.append({
                        "id_retiro": retiro.obtener_id_movimiento(),
                        "fecha": retiro.obtener_fecha(),
                        "cantidad": cantidad
                    })

        return {
            "id_remesa": remesa.obtener_id_remesa(),
            "material": remesa.obtener_material(),
            "id_proveedor": remesa.obtener_id_proveedor(),
            "cantidad_recibida": remesa.obtener_cantidad_recibida(),
            "precio_unitario": remesa.obtener_precio_unitario(),
            "costo_total": remesa.costo_total(),
            "saldo_actual": remesa.obtener_saldo(),
            "fecha_vencimiento": remesa.obtener_fecha_vencimiento(),
            "ingreso": {
                "id_ingreso": ingreso_encontrado.obtener_id_movimiento(),
                "fecha": ingreso_encontrado.obtener_fecha(),
                "id_pedido": ingreso_encontrado.obtener_id_pedido(),
                "id_renglon_pedido": remesa.obtener_id_renglon_pedido()
            },
            "retiros": retiros
        }
    def actualizar_estados_pedidos(self):
        for pedido in self.pedidos.values():
            pedido.actualizar_vencimiento()

        for id_proveedor, proveedor in self.proveedores.items():
            pendientes = []

            for pedido in self.pedidos.values():
                if pedido.obtener_id_proveedor()==id_proveedor:
                    if pedido.obtener_estado() in [
                        "Solicitado","Aceptado","En proceso"
                    ]:
                        pendientes.append(pedido)

            proveedor.guardar_pedidos_pendientes(pendientes)

    def buscar_pedido(self,id_pedido):
        if id_pedido not in self.pedidos:
            raise EntidadNoEncontradaError(
                f"No existe un pedido con el identificador {id_pedido}."
            )

        return self.pedidos[id_pedido]

    def aceptar_pedido(self,id_pedido):
        self.actualizar_estados_pedidos()
        pedido = self.buscar_pedido(id_pedido)
        pedido.aceptar()

    def rechazar_pedido(self,id_pedido,motivo):
        self.actualizar_estados_pedidos()
        pedido = self.buscar_pedido(id_pedido)
        pedido.rechazar(motivo)
        self.actualizar_estados_pedidos()

    def consultar_estado_pedido(self,id_pedido):
        self.actualizar_estados_pedidos()
        pedido = self.buscar_pedido(id_pedido)

        return {
            "id_pedido": pedido.obtener_id_pedido(),
            "estado": pedido.obtener_estado(),
            "fecha_solicitud": pedido.obtener_fecha_solicitud(),
            "plazo_entrega": pedido.obtener_plazo_entrega(),
            "fecha_limite_entrega": pedido.obtener_fecha_limite_entrega(),
            "motivo_rechazo": pedido.obtener_motivo_rechazo()
        }

    # Validaciones de cada dato a medida que se ingresa por el menu.

    @staticmethod
    def validar_id_proveedor_nuevo(id_proveedor):
        Proveedor.validar_id(id_proveedor)

    @staticmethod
    def validar_nombre_proveedor(nombre):
        Proveedor.validar_nombre(nombre)

    @staticmethod
    def validar_plazo_entrega_proveedor(plazo_entrega):
        Proveedor.validar_plazo_entrega(plazo_entrega)

    @staticmethod
    def validar_mail_proveedor(mail):
        Proveedor.validar_mail(mail)

    @staticmethod
    def validar_telefono_proveedor(telefono):
        Proveedor.validar_telefono(telefono)

    @staticmethod
    def validar_id_material_nuevo(id_material):
        Material.validar_id(id_material)

    @staticmethod
    def validar_nombre_material(nombre):
        Material.validar_nombre(nombre)

    @staticmethod
    def validar_unidad_material(unidad):
        Material.validar_unidad(unidad)

    @staticmethod
    def validar_punto_reposicion(punto_reposicion):
        Material.validar_punto_reposicion(punto_reposicion)

    @staticmethod
    def validar_id_pedido_nuevo(id_pedido):
        Pedido.validar_id(id_pedido)

    @staticmethod
    def validar_id_renglon_pedido_nuevo(renglones, id_renglon):
        Renglon_pedido.validar_id(id_renglon)
        Pedido.validar_id_renglon_nuevo(renglones, id_renglon)

    def validar_material_renglon_pedido(self, renglones, material):
        Renglon_pedido.validar_material(material)
        self.validar_material_en_deposito(material)
        Pedido.validar_material_renglon_nuevo(renglones, material)

    @staticmethod
    def validar_cantidad_pedida(cantidad):
        Renglon_pedido.validar_cantidad(cantidad)

    @staticmethod
    def crear_renglon_pedido(id_renglon, material, cantidad):
        return Renglon_pedido(id_renglon, material, cantidad)

    def validar_material_en_deposito(self, material):
        self.deposito[0].validar_material_registrado(material)

    @staticmethod
    def validar_id_ingreso_nuevo(id_movimiento):
        Movimiento_ingreso.validar_id(id_movimiento)

    @staticmethod
    def validar_id_remesa_nueva(id_remesa):
        Remesa.validar_id(id_remesa)

    def validar_material_remesa(self, material):
        Remesa.validar_material(material)
        self.validar_material_en_deposito(material)

    @staticmethod
    def validar_cantidad_recibida(cantidad_recibida):
        Remesa.validar_cantidad_recibida(cantidad_recibida)

    @staticmethod
    def validar_precio_unitario(precio_unitario):
        Remesa.validar_precio_unitario(precio_unitario)

    @staticmethod
    def validar_fecha_vencimiento(fecha_vencimiento, fecha_recepcion):
        Remesa.validar_vencimiento_no_pasado(fecha_vencimiento)
        Remesa.validar_fecha_vencimiento(fecha_vencimiento, fecha_recepcion)

    @staticmethod
    def validar_id_retiro_nuevo(id_movimiento):
        Movimiento_retiro.validar_id(id_movimiento)

    def validar_material_renglon_retiro(self, renglones, material):
        RenglonRetiro.validar_material(material)
        self.validar_material_en_deposito(material)
        Movimiento_retiro.validar_material_renglon_nuevo(renglones, material)

    def validar_cantidad_retiro(self, material, cantidad, fecha):
        RenglonRetiro.validar_cantidad(cantidad)
        self.deposito[0].validar_existencia_para_retiro(material, cantidad, fecha)

    @staticmethod
    def crear_renglon_retiro(material, cantidad):
        return RenglonRetiro(material, cantidad)