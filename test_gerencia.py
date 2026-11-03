from datetime import date, timedelta

import pytest

from gerencia import Gerencia
from deposito import Deposito
from proveedor import Proveedor
from material import Material
from pedido import Pedido
from renglon_pedido import Renglon_pedido
from renglon_retiro import RenglonRetiro
from remesa import Remesa
from movimiento_ingreso import Movimiento_ingreso
from movimiento_retiro import Movimiento_retiro
from conftest import fecha
from exceptions import (
    ProveedorNoRegistradoError,
    MaterialNoRegistradoError,
    MaterialNoIndicadoError,
    NombreDeMaterialDuplicadoError,
    NombreDeMaterialVacioError,
    IdentificadorDeMaterialDuplicadoError,
    IdentificadorDeProveedorDuplicadoError,
    IdentificadorDePedidoDuplicadoError,
    IdentificadorDeRemesaDuplicadoError,
    IdentificadorDeMovimientoDuplicadoError,
    CorreoElectronicoInvalidoError,
    MaterialRecibidoDistintoDelPedidoError,
    CantidadRecibidaDistintaDeLaPedidaError,
    RenglonDePedidoPendienteNoEncontradoError,
    EntidadNoEncontradaError,
    EstadoInvalidoError,
    EstadoDePedidoInvalidoError,
    FechaDeRecepcionAnteriorAlPedidoError,
    FechaDeRecepcionFuturaError,
    FechaDeVencimientoPasadaError,
)


def ingresar(g, id_mov, id_remesa, material, id_renglon, cantidad, **opcionales):
    g.almacenar_remesa(id_mov, id_remesa, material, 1, id_renglon, cantidad, fecha(), **opcionales)


# --- registros --------------------------------------------------------------

def test_crear_deposito():
    g = Gerencia([], {}, {}, {}, {})

    g.crear_deposito({}, {})

    assert len(g.obtener_deposito()) == 1
    assert isinstance(g.obtener_deposito()[0], Deposito)


def test_registrar_proveedor(gerencia):
    proveedor = gerencia.obtener_proveedores()[1]

    assert proveedor.nombre == "Proveedor SA"
    assert Proveedor.obtener_lista_id() == [1]


def test_registrar_proveedor_id_repetido(gerencia):
    with pytest.raises(IdentificadorDeProveedorDuplicadoError):
        gerencia.registrar_proveedor(1, "Otro", 3, None, None)


def test_registrar_proveedor_con_datos_invalidos_no_lo_guarda(gerencia):
    with pytest.raises(CorreoElectronicoInvalidoError):
        gerencia.registrar_proveedor(2, "Otro", 3, "mal-mail", None)

    assert 2 not in gerencia.obtener_proveedores()
    assert 2 not in Proveedor.obtener_lista_id()


def test_registrar_material(gerencia):
    materiales = gerencia.obtener_deposito()[0].obtener_materiales()

    assert set(materiales) == {1, 2}
    assert gerencia.material_registrado("  ALUMINIO ")


def test_registrar_material_nombre_repetido(gerencia):
    with pytest.raises(NombreDeMaterialDuplicadoError):
        gerencia.registrar_material(3, " Aluminio ", "kg", 4)


def test_registrar_material_id_repetido(gerencia):
    with pytest.raises(IdentificadorDeMaterialDuplicadoError):
        gerencia.registrar_material(1, "cobre", "kg", 4)


def test_registrar_material_nombre_invalido(gerencia):
    with pytest.raises(NombreDeMaterialVacioError):
        gerencia.registrar_material(3, None, "kg", 4)


# --- pedidos ----------------------------------------------------------------

def test_generar_pedido(gerencia):
    renglones = [Renglon_pedido(1, "aluminio", 20, 100)]

    gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 1, renglones, 5))

    pedido = gerencia.obtener_pedidos()[1]
    assert pedido.obtener_estado() == "Solicitado"
    assert gerencia.obtener_proveedores()[1].obtener_pedidos_pendientes() == [pedido]
    assert Pedido.obtener_lista_id() == [1]
    assert Renglon_pedido.obtener_lista_id() == [1]


def test_generar_pedido_proveedor_inexistente(gerencia):
    with pytest.raises(ProveedorNoRegistradoError):
        gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 99, [Renglon_pedido(1, "aluminio", 1, 1)], 5))


def test_generar_pedido_material_no_registrado(gerencia):
    with pytest.raises(MaterialNoRegistradoError):
        gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 1, [Renglon_pedido(1, "cobre", 1, 1)], 5))
    assert gerencia.obtener_pedidos() == {}


def test_generar_pedido_id_repetido(gerencia_con_pedido_aceptado):
    with pytest.raises(IdentificadorDePedidoDuplicadoError):
        gerencia_con_pedido_aceptado.registrar_pedido(gerencia_con_pedido_aceptado.crear_borrador_pedido(1, 1, [Renglon_pedido(3, "aluminio", 1, 1)], 5))


def test_aceptar_y_consultar_pedido(gerencia_con_pedido_aceptado):
    estado = gerencia_con_pedido_aceptado.consultar_estado_pedido(1)

    assert estado == {"id_pedido": 1, "estado": "Aceptado", "fecha_solicitud": date.today(), "motivo_rechazo": None}


def test_rechazar_pedido_lo_saca_de_pendientes(gerencia):
    gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 1, [Renglon_pedido(1, "aluminio", 1, 1)], 5))

    gerencia.rechazar_pedido(1, "precio")

    assert gerencia.consultar_estado_pedido(1)["motivo_rechazo"] == "precio"
    assert gerencia.obtener_proveedores()[1].obtener_pedidos_pendientes() == []


def test_buscar_pedido_inexistente(gerencia):
    with pytest.raises(EntidadNoEncontradaError):
        gerencia.buscar_pedido(99)
    with pytest.raises(EntidadNoEncontradaError):
        gerencia.aceptar_pedido(99)


# --- ingresos ---------------------------------------------------------------

def test_almacenar_remesa_parcial_deja_el_pedido_en_proceso(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado

    ingresar(g, 1, 1, " Aluminio ", 1, 20, fecha_vencimiento=fecha(30))

    remesa = g.obtener_deposito()[0].obtener_remesa(1)
    assert remesa.obtener_material() == "aluminio"
    assert remesa.obtener_fecha_vencimiento() == fecha(30)
    assert g.obtener_movimientos_de_ingreso()[1].obtener_id_pedido() == 1
    assert g.obtener_pedidos()[1].obtener_estado() == "En proceso"
    assert g.obtener_proveedores()[1].obtener_pedidos_pendientes() == [g.obtener_pedidos()[1]]
    assert Remesa.obtener_lista_id() == [1]
    assert Movimiento_ingreso.obtener_lista_id() == [1]


def test_almacenar_todas_las_remesas_completa_el_pedido(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado

    ingresar(g, 1, 1, "aluminio", 1, 20)
    ingresar(g, 2, 2, "titanio", 2, 8)

    assert g.obtener_pedidos()[1].obtener_estado() == "Recibido"
    assert g.obtener_proveedores()[1].obtener_pedidos_pendientes() == []
    assert g.consultar_existencia("titanio", date.today(), incluir_vencidas=False) == 8
    assert g.consultar_existencia("aluminio", date.today(), incluir_vencidas=True) == 20


def test_almacenar_remesa_de_pedido_no_aceptado(gerencia):
    gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 1, [Renglon_pedido(1, "aluminio", 20, 100)], 5))

    with pytest.raises(EstadoDePedidoInvalidoError):
        ingresar(gerencia, 1, 1, "aluminio", 1, 20)


def test_almacenar_remesa_material_distinto(gerencia_con_pedido_aceptado):
    with pytest.raises(MaterialRecibidoDistintoDelPedidoError):
        ingresar(gerencia_con_pedido_aceptado, 1, 1, "titanio", 1, 20)


def test_almacenar_remesa_material_no_registrado(gerencia_con_pedido_aceptado):
    with pytest.raises(MaterialNoRegistradoError):
        ingresar(gerencia_con_pedido_aceptado, 1, 1, "cobre", 1, 20)


@pytest.mark.parametrize("material", [None, "", "  "])
def test_almacenar_remesa_sin_material(gerencia_con_pedido_aceptado, material):
    with pytest.raises(MaterialNoIndicadoError):
        ingresar(gerencia_con_pedido_aceptado, 1, 1, material, 1, 20)


def test_almacenar_remesa_cantidad_distinta(gerencia_con_pedido_aceptado):
    with pytest.raises(CantidadRecibidaDistintaDeLaPedidaError):
        ingresar(gerencia_con_pedido_aceptado, 1, 1, "aluminio", 1, 19)


def test_almacenar_remesa_renglon_ya_ingresado(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado
    ingresar(g, 1, 1, "aluminio", 1, 20)

    with pytest.raises(RenglonDePedidoPendienteNoEncontradoError):
        ingresar(g, 2, 2, "aluminio", 1, 20)


def test_almacenar_remesa_proveedor_inexistente(gerencia_con_pedido_aceptado):
    with pytest.raises(ProveedorNoRegistradoError):
        gerencia_con_pedido_aceptado.almacenar_remesa(1, 1, "aluminio", 99, 1, 20, fecha())


def test_almacenar_remesa_fecha_anterior_al_pedido(gerencia_con_pedido_aceptado):
    with pytest.raises(FechaDeRecepcionAnteriorAlPedidoError):
        gerencia_con_pedido_aceptado.almacenar_remesa(1, 1, "aluminio", 1, 1, 20, fecha(-1))


def test_almacenar_remesa_fecha_futura_no_deja_nada_a_medias(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado

    with pytest.raises(FechaDeRecepcionFuturaError):
        g.almacenar_remesa(1, 1, "aluminio", 1, 1, 20, fecha(1))

    assert g.obtener_movimientos_de_ingreso() == {}
    assert g.obtener_deposito()[0].obtener_remesas() == {}
    assert g.obtener_pedidos()[1].obtener_renglones()[0].obtener_ingresado() is False


def test_almacenar_remesa_vencida_no_deja_nada_a_medias(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado
    g.obtener_pedidos()[1].fecha_solicitud = date.today() - timedelta(days=10)

    with pytest.raises(FechaDeVencimientoPasadaError):
        g.almacenar_remesa(1, 1, "aluminio", 1, 1, 20, fecha(-5), fecha_vencimiento=fecha(-2))

    assert g.obtener_deposito()[0].obtener_remesas() == {}
    assert Remesa.obtener_lista_id() == []
    assert Movimiento_ingreso.obtener_lista_id() == []


def test_validar_fecha_vencimiento_rechaza_vencidas_antes_que_el_control_de_recepcion(gerencia):
    with pytest.raises(FechaDeVencimientoPasadaError):
        gerencia.validar_fecha_vencimiento(fecha(-1), fecha())
    gerencia.validar_fecha_vencimiento(fecha(), fecha())
    gerencia.validar_fecha_vencimiento(None, fecha())


def test_almacenar_remesa_ids_repetidos(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado
    ingresar(g, 1, 1, "aluminio", 1, 20)

    with pytest.raises(IdentificadorDeMovimientoDuplicadoError):
        ingresar(g, 1, 2, "titanio", 2, 8)
    with pytest.raises(IdentificadorDeRemesaDuplicadoError):
        ingresar(g, 2, 1, "titanio", 2, 8)


# --- retiros y trazabilidad -------------------------------------------------

@pytest.fixture
def gerencia_con_stock(gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado
    ingresar(g, 1, 1, "aluminio", 1, 20)
    ingresar(g, 2, 2, "titanio", 2, 8)
    return g


def test_borrador_y_registro_de_retiro(gerencia_con_stock):
    g = gerencia_con_stock
    deposito = g.obtener_deposito()[0]

    retiro = g.crear_borrador_retiro(1, fecha(), [RenglonRetiro("aluminio", 15)])
    assert g.obtener_movimientos_de_egreso() == {}
    assert Movimiento_retiro.obtener_lista_id() == []
    assert deposito.existencia_disponible("aluminio") == 20

    g.registrar_retiro(retiro)

    assert retiro.obtener_estado() == "retirado"
    assert g.obtener_movimientos_de_egreso()[1] is retiro
    assert Movimiento_retiro.obtener_lista_id() == [1]
    assert deposito.existencia_disponible("aluminio") == 5


def test_trazabilidad_retiro(gerencia_con_stock):
    g = gerencia_con_stock
    g.registrar_retiro(g.crear_borrador_retiro(1, fecha(), [RenglonRetiro("aluminio", 15)]))

    traza = g.consultar_trazabilidad_retiro(1)

    assert traza["estado"] == "retirado"
    assert traza["renglones"] == [{"material": "aluminio", "cantidad": 15}]
    assert traza["remesas"] == [{"id_remesa": 1, "material": "aluminio", "cantidad": 15}]


def test_trazabilidad_de_retiro_en_borrador_o_inexistente(gerencia_con_stock):
    g = gerencia_con_stock
    g.crear_borrador_retiro(1, fecha(), [RenglonRetiro("aluminio", 1)])

    with pytest.raises(EntidadNoEncontradaError):
        g.consultar_trazabilidad_retiro(1)
    with pytest.raises(EntidadNoEncontradaError):
        g.consultar_trazabilidad_retiro(99)


def test_trazabilidad_remesa_incluye_agotadas(gerencia_con_stock):
    g = gerencia_con_stock
    g.registrar_retiro(g.crear_borrador_retiro(1, fecha(), [RenglonRetiro("titanio", 8)]))

    traza = g.consultar_trazabilidad_remesa(2)

    assert traza["saldo_actual"] == 0
    assert traza["ingreso"] == {"id_ingreso": 2, "fecha": fecha(), "id_pedido": 1, "id_renglon_pedido": 2}
    assert traza["retiros"] == [{"id_retiro": 1, "fecha": fecha(), "cantidad": 8}]


def test_trazabilidad_remesa_inexistente(gerencia_con_stock):
    with pytest.raises(EntidadNoEncontradaError):
        gerencia_con_stock.consultar_trazabilidad_remesa(99)


# --- reposicion -------------------------------------------------------------

def test_consultar_reposicion(gerencia_con_stock):
    datos = gerencia_con_stock.consultar_reposicion("  ALUMINIO ")

    assert datos["existencia"] == 20
    assert datos["requiere_reposicion"] is False


@pytest.mark.parametrize("nombre", [None, "", "  ", 5])
def test_consultar_reposicion_sin_nombre(gerencia, nombre):
    with pytest.raises(MaterialNoIndicadoError):
        gerencia.consultar_reposicion(nombre)


def test_consultar_reposicion_material_inexistente(gerencia):
    with pytest.raises(MaterialNoRegistradoError):
        gerencia.consultar_reposicion("cobre")


def test_materiales_a_reponer(gerencia):
    nombres = [d["nombre"] for d in gerencia.obtener_materiales_a_reponer()]

    assert nombres == ["aluminio", "titanio"]
