import pytest

from renglon_pedido import Renglon_pedido
from exceptions import (
    IdentificadorDeRenglonDePedidoInvalidoError,
    IdentificadorDeRenglonDePedidoDuplicadoError,
    MaterialNoIndicadoError,
    CantidadPedidaNoEnteraError,
    CantidadPedidaNoPositivaError,
    PrecioUnitarioNoPositivoError,
    MaterialRecibidoDistintoDelPedidoError,
    CantidadRecibidaDistintaDeLaPedidaError,
)


def test_creacion_renglon_pedido_valida():
    renglon = Renglon_pedido(1, "aluminio", 3, 50)

    assert renglon.obtener_id_renglon_pedido() == 1
    assert renglon.obtener_material() == "aluminio"
    assert renglon.obtener_cantidad() == 3
    assert renglon.obtener_precio_unitario() == 50
    assert renglon.obtener_ingresado() is False


@pytest.mark.parametrize("id_renglon", [0, -1, "R1", None, 2.0])
def test_id_invalido(id_renglon):
    with pytest.raises(IdentificadorDeRenglonDePedidoInvalidoError):
        Renglon_pedido(id_renglon, "aluminio", 3, 50)


def test_id_duplicado():
    Renglon_pedido.registrar_id(1)

    with pytest.raises(IdentificadorDeRenglonDePedidoDuplicadoError):
        Renglon_pedido(1, "titanio", 1, 10)


@pytest.mark.parametrize("material", ["", "  ", None, 7])
def test_material_invalido(material):
    with pytest.raises(MaterialNoIndicadoError):
        Renglon_pedido(1, material, 3, 50)


@pytest.mark.parametrize("cantidad", [2.5, "3", None])
def test_cantidad_no_entera(cantidad):
    with pytest.raises(CantidadPedidaNoEnteraError):
        Renglon_pedido(1, "aluminio", cantidad, 50)


@pytest.mark.parametrize("cantidad", [0, -1])
def test_cantidad_no_positiva(cantidad):
    with pytest.raises(CantidadPedidaNoPositivaError):
        Renglon_pedido(1, "aluminio", cantidad, 50)


@pytest.mark.parametrize("precio", [0, -1, "50", None])
def test_precio_invalido(precio):
    with pytest.raises(PrecioUnitarioNoPositivoError):
        Renglon_pedido(1, "aluminio", 3, precio)


def test_precio_decimal_es_valido():
    renglon = Renglon_pedido(1, "aluminio", 4, 12.5)

    assert renglon.subtotal_renglon() == 50


def test_subtotal_renglon():
    assert Renglon_pedido(1, "aluminio", 4, 25).subtotal_renglon() == 100


def test_modificar_ingresado():
    renglon = Renglon_pedido(1, "aluminio", 4, 25)

    renglon.modificar_ingresado()

    assert renglon.obtener_ingresado() is True


def test_validar_material_recibido_normaliza():
    renglon = Renglon_pedido(1, "Aluminio  AL-01", 4, 25)

    renglon.validar_material_recibido("  aluminio al-01 ")


def test_validar_material_recibido_distinto():
    renglon = Renglon_pedido(1, "aluminio", 4, 25)

    with pytest.raises(MaterialRecibidoDistintoDelPedidoError):
        renglon.validar_material_recibido("titanio")


def test_validar_cantidad_recibida():
    renglon = Renglon_pedido(1, "aluminio", 4, 25)

    renglon.validar_cantidad_recibida(4)
    with pytest.raises(CantidadRecibidaDistintaDeLaPedidaError):
        renglon.validar_cantidad_recibida(3)
