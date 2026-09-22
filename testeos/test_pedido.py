import pytest

from pedido import Pedido
from renglon_pedido import RenglonPedido
from exceptions import CantidadInvalidaError, PlazoEntregaInvalidoError, PrecioInvalidoError


def test_creacion_pedido_valido_arranca_sin_renglones_y_pendiente():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)

    assert pedido.renglones == []
    assert pedido.estado == "pendiente"


def test_pedido_sin_proveedor_lanza_error():
    with pytest.raises(ValueError):
        Pedido("PED-1", proveedor=None, plazo_entrega=5)


def test_pedido_plazo_entrega_cero_lanza_error():
    with pytest.raises(PlazoEntregaInvalidoError):
        Pedido("PED-1", proveedor="P1", plazo_entrega=0)


def test_pedido_plazo_entrega_negativo_lanza_error():
    with pytest.raises(PlazoEntregaInvalidoError):
        Pedido("PED-1", proveedor="P1", plazo_entrega=-1)


def test_pedidos_no_comparten_la_lista_de_renglones():
    # Regresión: si renglones=[] estuviera en la firma como default
    # mutable, ambos pedidos terminarían compartiendo la misma lista.
    p1 = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    p2 = Pedido("PED-2", proveedor="P1", plazo_entrega=5)

    p1.generar_renglon(RenglonPedido(1, "AL-01", 10, 100))

    assert len(p1.renglones) == 1
    assert len(p2.renglones) == 0


def test_generar_renglon_agrega_a_la_lista():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    pedido.generar_renglon(RenglonPedido(1, "AL-01", 10, 100))

    assert len(pedido.renglones) == 1


def test_subtotal_pedido_suma_los_subtotales_de_renglones():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    pedido.generar_renglon(RenglonPedido(1, "AL-01", 10, 100))  # 1000
    pedido.generar_renglon(RenglonPedido(2, "AL-02", 5, 50))    # 250

    assert pedido.subtotal_pedido() == 1250


def test_subtotal_pedido_sin_renglones_es_cero():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    assert pedido.subtotal_pedido() == 0


def test_cambiar_estado_valido():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    pedido.cambiar_estado("confirmado")
    assert pedido.estado == "confirmado"


def test_cambiar_estado_invalido_lanza_error():
    pedido = Pedido("PED-1", proveedor="P1", plazo_entrega=5)
    with pytest.raises(ValueError):
        pedido.cambiar_estado("no_existe")


# ---------------------------------------------------------------------------
# RenglonPedido
# ---------------------------------------------------------------------------

def test_creacion_renglon_pedido_valido_y_subtotal():
    renglon = RenglonPedido(1, "AL-01", cantidad=3, precio_unitario=50)
    assert renglon.subtotal_renglon() == 150


def test_renglon_pedido_sin_material_lanza_error():
    with pytest.raises(ValueError):
        RenglonPedido(1, None, cantidad=3, precio_unitario=50)


def test_renglon_pedido_cantidad_invalida_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        RenglonPedido(1, "AL-01", cantidad=0, precio_unitario=50)


def test_renglon_pedido_precio_invalido_lanza_error():
    with pytest.raises(PrecioInvalidoError):
        RenglonPedido(1, "AL-01", cantidad=3, precio_unitario=0)