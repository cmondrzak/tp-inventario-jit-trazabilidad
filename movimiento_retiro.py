from renglon_retiro import RenglonRetiro
from validaciones import Validaciones
from exceptions import IdentificadorDeMovimientoInvalidoError
from exceptions import IdentificadorDeMovimientoDuplicadoError
from exceptions import FormatoDeFechaInvalidoError
from exceptions import MaterialInvalidoError
from exceptions import MaterialRepetidoEnElRetiroError
from exceptions import CantidadARetirarNoPositivaError
from exceptions import RetiroYaRealizadoError
from exceptions import RetiroSinRenglonesError
from exceptions import RenglonesDelRetiroNoSonUnaListaError
from exceptions import ElementoNoEsUnRenglonDeRetiroError
from exceptions import FechaDeRetiroFuturaError
from exceptions import MaterialNoIndicadoError
from datetime import date, datetime


class Movimiento_retiro:
    lista_id=[]
    def __init__(self, id_movimiento, fecha, renglones_retiro, deposito, metodo_descarga, estado="no retirado"):
        Movimiento_retiro.validar_id(id_movimiento)
        Movimiento_retiro.validar_fecha(fecha)

        if not isinstance(renglones_retiro, list):
            raise RenglonesDelRetiroNoSonUnaListaError(f"Los renglones del retiro tienen que venir en una lista, pero se recibió un objeto de tipo {type(renglones_retiro).__name__}.")

        if len(renglones_retiro) == 0:
            raise RetiroSinRenglonesError("Un retiro tiene que incluir al menos un renglón, pero la lista recibida está vacía.")

        for renglon in renglones_retiro:
            if not isinstance(renglon, RenglonRetiro):
                raise ElementoNoEsUnRenglonDeRetiroError(f"Todos los elementos de la lista tienen que ser renglones de retiro, pero se encontró un objeto de tipo {type(renglon).__name__}.")

        renglones_revisados = []
        materiales = []
        for renglon in renglones_retiro:
            Movimiento_retiro.validar_material_renglon_nuevo(renglones_revisados, renglon.obtener_material())
            renglones_revisados.append(renglon)
            materiales.append(Validaciones.normalizar_texto(renglon.obtener_material()))

        self.fecha = fecha
        self.deposito = deposito
        self.metodo_descarga = metodo_descarga

        remesas_modificadas = []
        for renglon in renglones_retiro:
            plan = self._planificar_consumo(
                Validaciones.normalizar_texto(renglon.obtener_material()),
                renglon.obtener_cantidad_solicitada()
            )
            for consumo in plan:
                remesas_modificadas.append(consumo)

        self.id_movimiento = id_movimiento
        self.renglones_retiro = list(renglones_retiro)
        self.remesas_modificadas = remesas_modificadas
        self.materiales_modificados = materiales
        self.estado = estado

    @staticmethod
    def validar_id(id_movimiento):
        if not Validaciones.es_identificador_valido(id_movimiento):
            raise IdentificadorDeMovimientoInvalidoError(f"El identificador del movimiento debe ser un número entero positivo; se recibió {id_movimiento!r}.")
        if not Validaciones.validarid(Movimiento_retiro.lista_id,id_movimiento):
            raise IdentificadorDeMovimientoDuplicadoError(f"Ya existe un movimiento de retiro con el identificador {id_movimiento!r}.")

    @staticmethod
    def validar_fecha(fecha):
        if not Validaciones.es_fecha(fecha):
            raise FormatoDeFechaInvalidoError(f"La fecha del retiro debe escribirse como dd/mm/aaaa y ser una fecha real; se recibió {fecha!r}.")
        if datetime.strptime(fecha.strip(), "%d/%m/%Y").date() > date.today():
            raise FechaDeRetiroFuturaError(f"La fecha del retiro {fecha} es posterior a hoy; no se puede retirar material en una fecha que todavía no llegó.")

    @staticmethod
    def validar_material_renglon_nuevo(renglones, material):
        buscado = Validaciones.normalizar_texto(material)
        for renglon in renglones:
            if Validaciones.normalizar_texto(renglon.obtener_material()) == buscado:
                raise MaterialRepetidoEnElRetiroError(f"El material '{buscado}' ya está en otro renglón; cada material se retira en un único renglón.")

    def eliminar_renglon(self,material):
        if self.estado!="no retirado":
            raise RetiroYaRealizadoError("No se pueden quitar renglones de un retiro que ya fue realizado.")

        if not Validaciones.es_texto_no_vacio(material):
            raise MaterialNoIndicadoError(f"Hay que indicar como texto el material del renglón a quitar; se recibió {material!r}.")

        material = Validaciones.normalizar_texto(material)

        for renglon in self.renglones_retiro:
            if Validaciones.normalizar_texto(renglon.obtener_material())==material:
                if len(self.renglones_retiro)==1:
                    raise RetiroSinRenglonesError(
                        "No se puede eliminar el unico renglon del retiro."
                    )

                remesas_restantes=[]
                for tup in self.remesas_modificadas:
                    if Validaciones.normalizar_texto(tup[0].obtener_material())!=material:
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

        self.deposito.validar_material_registrado(material)
        self.deposito.validar_existencia_para_retiro(material, cantidad, self.fecha)

        disponibles = self.deposito.remesas_por_material(
            material,
            self.fecha
        )

        ordenadas = self.metodo_descarga(disponibles)
        plan = []
        faltante = cantidad
        def armar_plan(ordenadas,plan, faltante):
            remesa = ordenadas[0]
            saldo = remesa.obtener_saldo()
            
            if saldo < faltante:
                cantidad_a_retirar = saldo
                plan.append((remesa,cantidad_a_retirar))
                faltante -= saldo
                armar_plan(ordenadas[1:],plan,faltante)
            else:
                cantidad_a_retirar = faltante
                plan.append((remesa,cantidad_a_retirar))
            
            return plan    
        
        return armar_plan(ordenadas, plan, faltante)
            
        
    def cambiar_estado(self):
        if self.estado != "no retirado":
            raise RetiroYaRealizadoError(
                "El retiro ya fue realizado; no se puede volver a confirmar."
            )

        plan_completo = []

        for renglon in self.renglones_retiro:
            plan = self._planificar_consumo(
                renglon.obtener_material(),
                renglon.obtener_cantidad_solicitada()
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
    def registrar_id(cls, identificador):
        cls.lista_id.append(identificador)

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

        RenglonRetiro.validar_material(material)
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

    def obtener_estado(self):
        return self.estado

    def obtener_renglones(self):
        return self.renglones_retiro.copy()

    def obtener_remesas_modificadas(self):
        return self.remesas_modificadas.copy()

    def obtener_fecha(self):
        return self.fecha

    def obtener_id_movimiento(self):
        return self.id_movimiento


        