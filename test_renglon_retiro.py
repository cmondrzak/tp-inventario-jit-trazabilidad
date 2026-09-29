import pytest

from renglon_retiro import RenglonRetiro
from exceptions import CantidadInvalidaError, MaterialNoEncontradoError


def test_creacion_renglon_retiro_valida():
    renglon = RenglonRetiro("AL-01", None, cantidad_solicitada=5)

    assert renglon.material == "AL-01"
    assert renglon.cantidad_solicitada == 5


def test_renglon_retiro_material_vacio_lanza_error():
    with pytest.raises(MaterialNoEncontradoError):
        RenglonRetiro("", None, 5)


def test_renglon_retiro_cantidad_solicitada_cero_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        RenglonRetiro("AL-01", None, 0)


def test_renglon_retiro_cantidad_solicitada_negativa_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        RenglonRetiro("AL-01", None, -3)


def test_modificar_remesa_consume_el_saldo():
    class RemesaFalsa:
        def __init__(self):
            self.saldo_disponible = 10

        def consumir(self, cantidad):
            self.saldo_disponible -= cantidad

    remesa = RemesaFalsa()
    renglon = RenglonRetiro("AL-01", remesa, 4)

    renglon.modificar_remesa(remesa)

    assert remesa.saldo_disponible == 6
