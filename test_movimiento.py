from datetime import date

import pytest

from movimiento import Movimiento
from exceptions import FechaInvalidaError, IdentificadorDuplicadoError


@pytest.fixture(autouse=True)
def reset_movimiento_state():
    Movimiento.lista_id = []


def test_creacion_movimiento_valido():
    movimiento = Movimiento(1, date(2026, 3, 1))

    assert movimiento.id_movimiento == 1
    assert movimiento.fecha == date(2026, 3, 1)


def test_movimiento_id_duplicado_lanza_error():
    Movimiento(1, date(2026, 3, 1))

    with pytest.raises(IdentificadorDuplicadoError):
        Movimiento(1, date(2026, 3, 2))


def test_movimiento_fecha_invalida_lanza_error():
    with pytest.raises(FechaInvalidaError):
        Movimiento(1, "2026-03-01")
