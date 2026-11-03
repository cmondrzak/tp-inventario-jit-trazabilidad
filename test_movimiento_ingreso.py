import pytest

from movimiento_ingreso import Movimiento_ingreso
from conftest import fecha
from exceptions import (
    IdentificadorDeMovimientoInvalidoError,
    IdentificadorDeMovimientoDuplicadoError,
    FormatoDeFechaInvalidoError,
    RemesaNoIndicadaEnElIngresoError,
    PedidoNoIndicadoEnElIngresoError,
)


def test_creacion_movimiento_ingreso_valido():
    mov = Movimiento_ingreso(1, fecha(), 10, 20)

    assert mov.obtener_id_movimiento() == 1
    assert mov.obtener_fecha() == fecha()
    assert mov.obtener_id_remesa() == 10
    assert mov.obtener_id_pedido() == 20


@pytest.mark.parametrize("id_mov", [0, -1, "M1", None])
def test_id_invalido(id_mov):
    with pytest.raises(IdentificadorDeMovimientoInvalidoError):
        Movimiento_ingreso(id_mov, fecha(), 10, 20)


def test_id_duplicado():
    Movimiento_ingreso.registrar_id(1)

    with pytest.raises(IdentificadorDeMovimientoDuplicadoError):
        Movimiento_ingreso(1, fecha(), 10, 20)


@pytest.mark.parametrize("valor", ["2026-03-01", "", None, "31/04/2026"])
def test_fecha_invalida(valor):
    with pytest.raises(FormatoDeFechaInvalidoError):
        Movimiento_ingreso(1, valor, 10, 20)


@pytest.mark.parametrize("remesa", [None, 0, "R-1"])
def test_remesa_no_indicada(remesa):
    with pytest.raises(RemesaNoIndicadaEnElIngresoError):
        Movimiento_ingreso(1, fecha(), remesa, 20)


@pytest.mark.parametrize("pedido", [None, 0, "PED-1"])
def test_pedido_no_indicado(pedido):
    with pytest.raises(PedidoNoIndicadoEnElIngresoError):
        Movimiento_ingreso(1, fecha(), 10, pedido)
