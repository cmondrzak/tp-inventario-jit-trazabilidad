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
from exceptions import ProveedorNoRegistradoError, MaterialNoRegistradoError, MaterialNoIndicadoError, NombreDeMaterialDuplicadoError, IdentificadorDeMovimientoDuplicadoError, MaterialRecibidoDistintoDelPedidoError, RenglonDePedidoPendienteNoEncontradoError, EntidadNoEncontradaError, EstadoInvalidoError
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
            Proveedor.registrar_id(id_proveedor)

    @staticmethod
    def existencia_disponible(deposito,material):
        return deposito.existencia_disponible(material)
        
    def generar_pedido(self,id_pedido,proveedor,renglones,plazo_entrega):
        self.validar_proveedor_registrado(proveedor)
        if isinstance(renglones, list):
            for renglon in renglones:
                if isinstance(renglon, Renglon_pedido) and not self.material_registrado(renglon.obtener_material()):
                    raise MaterialNoRegistradoError(f"No se puede pedir '{renglon.obtener_material()}' porque ese material todavía no fue registrado en el depósito.")
        p=Pedido(id_pedido,proveedor,renglones,plazo_entrega)
        self.proveedores[proveedor].agregar_pedido_pendiente(p)
        self.pedidos[id_pedido] = p
        p.registrar_ids()

    def generar_retiro(self, id_movimiento, fecha, deposito, renglones):
        retiro = Movimiento_retiro(
            id_movimiento,
            fecha,
            renglones,
            deposito,
            deposito.retirar_fefo
        )

        self.movimientos_de_egreso[id_movimiento] = retiro
        Movimiento_retiro.registrar_id(id_movimiento)
        return retiro
        
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
    
    
    def validar_proveedor_registrado(self, id_proveedor):
        if id_proveedor not in self.proveedores:
            raise ProveedorNoRegistradoError(f"No existe ningún proveedor registrado con el identificador {id_proveedor!r}.")

    def buscar_renglon_pendiente(self, id_proveedor, id_renglon_pedido):
        """Devuelve (pedido, renglon) del renglon sin ingresar con ese id entre los pedidos pendientes del proveedor."""
        self.validar_proveedor_registrado(id_proveedor)
        self.actualizar_estados_pedidos()
        for pedido in self.proveedores[id_proveedor].obtener_pedidos_pendientes():
            for renglon in pedido.obtener_renglones():
                if renglon.obtener_id_renglon_pedido() == id_renglon_pedido and not renglon.obtener_ingresado():
                    pedido.validar_recepcion()
                    return pedido, renglon
        raise RenglonDePedidoPendienteNoEncontradoError(f"El proveedor {id_proveedor!r} no tiene ningún pedido pendiente con el renglón {id_renglon_pedido!r} sin ingresar.")

    def almacenar_remesa(self,id_movimiento_ingreso, id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales):
        Movimiento_ingreso.validar_id(id_movimiento_ingreso)
        Remesa.validar_id(id_remesa)
        Remesa.validar_material(material)
        material = Validaciones.normalizar_texto(material)
        self.deposito[0].validar_material_registrado(material)

        pedido, renglon = self.buscar_renglon_pendiente(id_proveedor, id_renglon_pedido)
        renglon.validar_material_recibido(material)
        renglon.validar_cantidad_recibida(cantidad_recibida)
        pedido.validar_fecha_recepcion(fecha_recepcion)

        r = Proveedor.generar_remesa(id_remesa, material, id_proveedor, id_renglon_pedido, cantidad_recibida, fecha_recepcion, **datos_opcionales)
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
            "motivo_rechazo": pedido.obtener_motivo_rechazo()
        }