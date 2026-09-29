from datetime import date

import pytest

from movimiento_ingreso import movimiento_ingreso
from movimiento import Movimiento
from exceptions import IdentificadorDuplicadoError


@pytest.fixture(autouse=True)
def reset_movimiento_ingreso_state():
    Movimiento.lista_id = []
    movimiento_ingreso.lista_id = []


def test_creacion_movimiento_ingreso_valido():
    mov = movimiento_ingreso(1, date(2026, 3, 1), "R-1", None)

    assert mov.id_movimiento == 1
    assert mov.remesa == "R-1"
    assert mov.pedido is None


def test_movimiento_ingreso_remesa_vacia_lanza_error():
    with pytest.raises(ValueError, match="remesa"):
        movimiento_ingreso(1, date(2026, 3, 1), "", None)


def test_movimiento_ingreso_id_duplicado_lanza_error():
    movimiento_ingreso(1, date(2026, 3, 1), "R-1", None)

    with pytest.raises(IdentificadorDuplicadoError):
        movimiento_ingreso(1, date(2026, 3, 2), "R-2", None)
