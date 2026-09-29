from datetime import date

import pytest

from movimiento_retiro import Movimiento_retiro
from movimiento import Movimiento
from exceptions import IdentificadorDuplicadoError


@pytest.fixture(autouse=True)
def reset_movimiento_retiro_state():
    Movimiento.lista_id = []
    Movimiento_retiro.lista_id = []


def test_creacion_movimiento_retiro_valido():
    mov = Movimiento_retiro(1, date(2026, 3, 1), [])

    assert mov.id_movimiento == 1
    assert mov.renglones_retiro == []


def test_movimiento_retiro_id_duplicado_lanza_error():
    Movimiento_retiro(1, date(2026, 3, 1), [])

    with pytest.raises(IdentificadorDuplicadoError):
        Movimiento_retiro(1, date(2026, 3, 2), [])


def test_agregar_renglon_lo_suma_a_la_lista():
    mov = Movimiento_retiro(1, date(2026, 3, 1), [])

    mov.agregar_renglon("renglon-1")

    assert mov.renglones_retiro == ["renglon-1"]


def test_movimientos_no_comparten_la_lista_de_renglones():
    m1 = Movimiento_retiro(1, date(2026, 3, 1), [])
    m2 = Movimiento_retiro(2, date(2026, 3, 1), [])

    m1.agregar_renglon("renglon-1")

    assert m1.renglones_retiro == ["renglon-1"]
    assert m2.renglones_retiro == []
