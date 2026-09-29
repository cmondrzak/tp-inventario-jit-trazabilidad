import pytest

from proveedor import Proveedor
from exceptions import IdentificadorDuplicadoError, NombreInvalidoError


@pytest.fixture(autouse=True)
def reset_proveedor_state():
    Proveedor.lista_id = []


def test_creacion_proveedor_valida():
    proveedor = Proveedor("P1", "Proveedor SA", [], "contacto@proveedor.com", "12345678")

    assert proveedor.nombre == "Proveedor SA"
    assert proveedor.mail == "contacto@proveedor.com"
    assert proveedor.telefono == "12345678"
    assert proveedor.pedidios_pendientes == []


def test_proveedor_id_duplicado_lanza_error():
    Proveedor("P1", "Proveedor SA", [], "a@a.com", "111")

    with pytest.raises(IdentificadorDuplicadoError):
        Proveedor("P1", "Otro proveedor", [], "b@b.com", "222")


def test_proveedor_nombre_vacio_lanza_error():
    with pytest.raises(NombreInvalidoError):
        Proveedor("P1", "", [], "a@a.com", "111")


def test_proveedor_nombre_none_lanza_error():
    with pytest.raises(NombreInvalidoError):
        Proveedor("P1", None, [], "a@a.com", "111")


def test_agregar_pedido_pendiente():
    proveedor = Proveedor("P1", "Proveedor SA", [], "a@a.com", "111")

    proveedor.agregar_pedido_pendiente("PED-1")

    assert proveedor.pedidios_pendientes == ["PED-1"]


def test_borrar_pedido_pendiente():
    proveedor = Proveedor("P1", "Proveedor SA", ["PED-1"], "a@a.com", "111")

    proveedor.borrar_pedido_pendiente("PED-1")

    assert proveedor.pedidios_pendientes == []


def test_cambiar_estado_pedido_delega_en_el_pedido():
    class PedidoFalso:
        def __init__(self):
            self.estado = "pendiente"

        def cambiar_estado(self, nuevo_estado):
            self.estado = nuevo_estado

    pedido = PedidoFalso()
    Proveedor.cambiar_estado_pedido(pedido, "confirmado")

    assert pedido.estado == "confirmado"
