from datetime import date, timedelta

import pytest

from pedido import Pedido
from renglon_pedido import Renglon_pedido
from conftest import fecha
from exceptions import (
    IdentificadorDePedidoInvalidoError,
    IdentificadorDePedidoDuplicadoError,
    IdentificadorDeRenglonDePedidoDuplicadoError,
    ProveedorNoIndicadoError,
    RenglonesDelPedidoNoSonUnaListaError,
    PedidoSinRenglonesError,
    ElementoNoEsUnRenglonDePedidoError,
    MaterialRepetidoEnElPedidoError,
    EstadoDePedidoInvalidoError,
    FormatoDeFechaInvalidoError,
    FechaDeRecepcionAnteriorAlPedidoError,
    RenglonDePedidoNoEncontradoError,
)


def renglon(id_renglon=1, material="aluminio", cantidad=10):
    return Renglon_pedido(id_renglon, material, cantidad)


def crear_pedido(id_pedido=1, renglones=None):
    return Pedido(id_pedido, 1, renglones if renglones is not None else [renglon()])


# --- ingreso de datos -------------------------------------------------------

def test_creacion_pedido_valido():
    r = renglon()
    pedido = Pedido(1, 2, [r])

    assert pedido.obtener_id_pedido() == 1
    assert pedido.obtener_id_proveedor() == 2
    assert pedido.obtener_renglones() == [r]
    assert not hasattr(pedido, "plazo_entrega")
    assert pedido.obtener_estado() == "Solicitado"
    assert pedido.obtener_fecha_solicitud() == date.today()
    assert pedido.obtener_motivo_rechazo() is None


@pytest.mark.parametrize("id_pedido", [0, -1, "PED-1", None])
def test_id_invalido(id_pedido):
    with pytest.raises(IdentificadorDePedidoInvalidoError):
        Pedido(id_pedido, 1, [renglon()])


def test_id_duplicado():
    Pedido.registrar_id(1)

    with pytest.raises(IdentificadorDePedidoDuplicadoError):
        crear_pedido(1)


@pytest.mark.parametrize("proveedor", [None, 0, "P1"])
def test_proveedor_no_indicado(proveedor):
    with pytest.raises(ProveedorNoIndicadoError):
        Pedido(1, proveedor, [renglon()])


@pytest.mark.parametrize("renglones", [None, "renglon", (1,), {}])
def test_renglones_no_son_lista(renglones):
    with pytest.raises(RenglonesDelPedidoNoSonUnaListaError):
        Pedido(1, 1, renglones)


def test_pedido_sin_renglones():
    with pytest.raises(PedidoSinRenglonesError):
        Pedido(1, 1, [])


def test_elemento_no_es_renglon():
    with pytest.raises(ElementoNoEsUnRenglonDePedidoError):
        Pedido(1, 1, [renglon(), "otro"])


def test_renglones_con_id_repetido():
    r1 = renglon(1, "aluminio")
    r2 = renglon(2, "titanio")
    r2.id_renglon = 1

    with pytest.raises(IdentificadorDeRenglonDePedidoDuplicadoError):
        Pedido(1, 1, [r1, r2])


def test_renglones_con_material_repetido_normalizado():
    with pytest.raises(MaterialRepetidoEnElPedidoError):
        Pedido(1, 1, [renglon(1, "Aluminio"), renglon(2, "  aluminio ")])


def test_crear_pedido_no_registra_ids_hasta_registrar_ids():
    pedido = Pedido(1, 1, [renglon(1), renglon(2, "titanio")])
    assert Pedido.obtener_lista_id() == []

    pedido.registrar_ids()

    assert Pedido.obtener_lista_id() == [1]
    assert Renglon_pedido.obtener_lista_id() == [1, 2]


# --- renglones --------------------------------------------------------------

def test_generar_renglon_agrega_al_final():
    pedido = crear_pedido()

    pedido.generar_renglon(2, "titanio", 5)

    renglones = pedido.obtener_renglones()
    assert [r.obtener_id_renglon_pedido() for r in renglones] == [1, 2]
    assert Renglon_pedido.obtener_lista_id() == []

    pedido.registrar_ids()
    assert Renglon_pedido.obtener_lista_id() == [1, 2]


def test_generar_renglon_material_repetido():
    pedido = crear_pedido()

    with pytest.raises(MaterialRepetidoEnElPedidoError):
        pedido.generar_renglon(2, " ALUMINIO", 5)


def test_generar_renglon_con_id_ya_usado_en_el_pedido():
    pedido = crear_pedido()

    with pytest.raises(IdentificadorDeRenglonDePedidoDuplicadoError):
        pedido.generar_renglon(1, "titanio", 5)


def test_generar_renglon_en_pedido_aceptado():
    pedido = crear_pedido()
    pedido.aceptar()

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.generar_renglon(2, "titanio", 5)


def test_eliminar_renglon_pedido():
    pedido = crear_pedido(renglones=[renglon(1, "aluminio"), renglon(2, "titanio")])

    pedido.eliminar_renglon_pedido(1)

    assert [r.obtener_id_renglon_pedido() for r in pedido.obtener_renglones()] == [2]


def test_eliminar_unico_renglon():
    pedido = crear_pedido()

    with pytest.raises(PedidoSinRenglonesError):
        pedido.eliminar_renglon_pedido(1)


def test_eliminar_renglon_inexistente():
    pedido = crear_pedido(renglones=[renglon(1, "aluminio"), renglon(2, "titanio")])

    with pytest.raises(RenglonDePedidoNoEncontradoError):
        pedido.eliminar_renglon_pedido(99)


def test_eliminar_renglon_en_pedido_rechazado():
    pedido = crear_pedido(renglones=[renglon(1, "aluminio"), renglon(2, "titanio")])
    pedido.rechazar("sin stock")

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.eliminar_renglon_pedido(1)


# --- estados ----------------------------------------------------------------

def test_aceptar():
    pedido = crear_pedido()

    pedido.aceptar()

    assert pedido.obtener_estado() == "Aceptado"


def test_aceptar_dos_veces():
    pedido = crear_pedido()
    pedido.aceptar()

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.aceptar()


def test_rechazar_guarda_el_motivo_sin_espacios():
    pedido = crear_pedido()

    pedido.rechazar("  sin stock  ")

    assert pedido.obtener_estado() == "Rechazado"
    assert pedido.obtener_motivo_rechazo() == "sin stock"


@pytest.mark.parametrize("motivo", ["", "   ", None, 3])
def test_rechazar_sin_motivo(motivo):
    pedido = crear_pedido()

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.rechazar(motivo)
    assert pedido.obtener_estado() == "Solicitado"


def test_rechazar_pedido_aceptado():
    pedido = crear_pedido()
    pedido.aceptar()

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.rechazar("tarde")


def test_vencimiento_a_los_30_dias():
    pedido = crear_pedido()
    pedido.fecha_inicio_espera = date.today() - timedelta(days=30)

    pedido.actualizar_vencimiento()

    assert pedido.obtener_estado() == "Rechazado"
    assert "30 dias" in pedido.obtener_motivo_rechazo()


def test_no_vence_a_los_29_dias():
    pedido = crear_pedido()
    pedido.fecha_inicio_espera = date.today() - timedelta(days=29)

    pedido.actualizar_vencimiento()

    assert pedido.obtener_estado() == "Solicitado"


def test_aceptar_pedido_vencido():
    pedido = crear_pedido()
    pedido.fecha_inicio_espera = date.today() - timedelta(days=31)

    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.aceptar()


def test_pedido_aceptado_no_vence():
    pedido = crear_pedido()
    pedido.aceptar()
    pedido.fecha_inicio_espera = date.today() - timedelta(days=60)

    pedido.actualizar_vencimiento()

    assert pedido.obtener_estado() == "Aceptado"


def test_validar_recepcion_solo_aceptado_o_en_proceso():
    pedido = crear_pedido()
    with pytest.raises(EstadoDePedidoInvalidoError):
        pedido.validar_recepcion()

    pedido.aceptar()
    pedido.validar_recepcion()


def test_actualizar_estado_recepcion():
    pedido = crear_pedido(renglones=[renglon(1, "aluminio"), renglon(2, "titanio")])
    pedido.aceptar()
    r1, r2 = pedido.obtener_renglones()

    r1.modificar_ingresado()
    pedido.actualizar_estado_recepcion()
    assert pedido.obtener_estado() == "En proceso"

    r2.modificar_ingresado()
    pedido.actualizar_estado_recepcion()
    assert pedido.obtener_estado() == "Recibido"


def test_validar_fecha_recepcion():
    pedido = crear_pedido()

    pedido.validar_fecha_recepcion(fecha())
    with pytest.raises(FechaDeRecepcionAnteriorAlPedidoError):
        pedido.validar_fecha_recepcion(fecha(-1))


@pytest.mark.parametrize("valor", ["2026-01-01", "", None, "31/02/2026"])
def test_validar_fecha_recepcion_formato_invalido(valor):
    pedido = crear_pedido()

    with pytest.raises(FormatoDeFechaInvalidoError):
        pedido.validar_fecha_recepcion(valor)
