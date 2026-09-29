import pytest

from pedido import Pedido
from exceptions import IdentificadorDuplicadoError, PedidoNoEncontradoError, PlazoEntregaInvalidoError


@pytest.fixture(autouse=True)
def reset_pedido_state():
    Pedido.lista_id = []


def test_creacion_pedido_valido():
    pedido = Pedido("PED-1", proveedor="P1", renglones=[], plazo_entrega=5, estado="pendiente")

    assert pedido.id_pedido == "PED-1"
    assert pedido.renglones == []
    assert pedido.estado == "pendiente"


def test_pedido_id_duplicado_lanza_error():
    Pedido("PED-1", "P1", [], 5, "pendiente")

    with pytest.raises(IdentificadorDuplicadoError):
        Pedido("PED-1", "P1", [], 5, "pendiente")


def test_pedido_sin_renglones_lanza_error():
    with pytest.raises(PedidoNoEncontradoError):
        Pedido("PED-1", "P1", [], 5, "pendiente")


def test_pedido_plazo_entrega_cero_lanza_error():
    with pytest.raises(PlazoEntregaInvalidoError):
        Pedido("PED-1", "P1", [], 0, "pendiente")


def test_pedido_plazo_entrega_negativo_lanza_error():
    with pytest.raises(PlazoEntregaInvalidoError):
        Pedido("PED-1", "P1", [], -1, "pendiente")


def test_generar_renglon_agrega_a_la_lista():
    pedido = Pedido("PED-1", "P1", [], 5, "pendiente")

    pedido.generar_renglon(1, "AL-01", 10, 100)

    assert len(pedido.renglones) == 1


def test_subtotal_suma_los_subtotales_de_los_renglones():
    pedido = Pedido("PED-1", "P1", [], 5, "pendiente")
    pedido.generar_renglon(1, "AL-01", 10, 100)
    pedido.generar_renglon(2, "AL-02", 5, 50)

    assert pedido.subtotal() == 1250


def test_cambiar_estado_actualiza_el_estado():
    pedido = Pedido("PED-1", "P1", [], 5, "pendiente")

    pedido.cambiar_estado("confirmado")

    assert pedido.estado == "confirmado"
