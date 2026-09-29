import pytest

from renglon_pedido import Renglon_pedido
from exceptions import CantidadInvalidaError, IdentificadorDuplicadoError, MaterialNoEncontradoError, PrecioInvalidoError


@pytest.fixture(autouse=True)
def reset_renglon_pedido_state():
    Renglon_pedido.lista_id = []


def test_creacion_renglon_pedido_valida_y_subtotal():
    renglon = Renglon_pedido(1, "AL-01", cantidad=3, precio_unitario=50)

    assert renglon.id_renglon == 1
    assert renglon.material == "AL-01"
    assert renglon.subtotal_renglon() == 150


def test_renglon_pedido_id_duplicado_lanza_error():
    Renglon_pedido(1, "AL-01", 3, 50)

    with pytest.raises(IdentificadorDuplicadoError):
        Renglon_pedido(1, "AL-02", 1, 10)


def test_renglon_pedido_material_vacio_lanza_error():
    with pytest.raises(MaterialNoEncontradoError):
        Renglon_pedido(1, "", 3, 50)


def test_renglon_pedido_cantidad_cero_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        Renglon_pedido(1, "AL-01", 0, 50)


def test_renglon_pedido_cantidad_negativa_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        Renglon_pedido(1, "AL-01", -1, 50)


def test_renglon_pedido_precio_unitario_cero_lanza_error():
    with pytest.raises(PrecioInvalidoError):
        Renglon_pedido(1, "AL-01", 3, 0)


def test_renglon_pedido_precio_unitario_negativo_lanza_error():
    with pytest.raises(PrecioInvalidoError):
        Renglon_pedido(1, "AL-01", 3, -1)


def test_subtotal_renglon_multiplica_cantidad_por_precio():
    renglon = Renglon_pedido(1, "AL-01", 4, 25)

    assert renglon.subtotal_renglon() == 100
