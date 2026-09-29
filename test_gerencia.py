import pytest

from gerencia import Gerencia
from deposito import Deposito
from proveedor import Proveedor


@pytest.fixture(autouse=True)
def reset_estado():
    Proveedor.lista_id = []


def test_registrar_proveedor_lo_deja_disponible_por_id():
    gerencia = Gerencia(Deposito({}, {}), {}, {}, {})

    gerencia.registrar_proveedor("P1", "Proveedor SA", "a@a.com", "111")

    assert gerencia.proveedores["P1"].nombre == "Proveedor SA"


def test_generar_pedido_lo_guarda_y_lo_agrega_al_proveedor():
    gerencia = Gerencia(Deposito({}, {}), {}, {}, {})
    proveedor = Proveedor("P1", "Proveedor SA", [], "a@a.com", "111")

    gerencia.generar_pedido("PED-1", proveedor, [], 5, "pendiente")

    assert gerencia.pedidos["PED-1"].proveedor is proveedor
    assert proveedor.pedidios_pendientes == [gerencia.pedidos["PED-1"]]


def test_obtener_pedidos_devuelve_el_diccionario_de_pedidos():
    pedidos = {}
    gerencia = Gerencia(Deposito({}, {}), pedidos, {}, {})

    assert gerencia.obtener_pedidos() is pedidos
