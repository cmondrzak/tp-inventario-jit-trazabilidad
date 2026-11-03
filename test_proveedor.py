import pytest

from proveedor import Proveedor
from pedido import Pedido
from remesa import Remesa
from renglon_pedido import Renglon_pedido
from conftest import fecha
from exceptions import (
    IdentificadorDeProveedorInvalidoError,
    IdentificadorDeProveedorDuplicadoError,
    NombreDeProveedorVacioError,
    PlazoDeEntregaNoEnteroError,
    PlazoDeEntregaNoPositivoError,
    CorreoElectronicoInvalidoError,
    NumeroDeTelefonoInvalidoError,
    ObjetoNoEsUnPedidoError,
    PedidoDeOtroProveedorError,
)


def crear_pedido(id_pedido, id_proveedor, id_renglon):
    return Pedido(id_pedido, id_proveedor, [Renglon_pedido(id_renglon, "aluminio", 5)], 5)


def test_creacion_proveedor_valida():
    proveedor = Proveedor(1, "Proveedor SA", 5, mail="contacto@proveedor.com", telefono="12345678")

    assert proveedor.obtener_idproveedor() == 1
    assert proveedor.obtener_nombre() == "Proveedor SA"
    assert proveedor.obtener_mail() == "contacto@proveedor.com"
    assert proveedor.obtener_telefono() == "12345678"
    assert proveedor.obtener_plazo_entrega() == 5
    assert proveedor.obtener_pedidos_pendientes() == []


def test_nombre_se_guarda_sin_espacios_de_mas():
    assert Proveedor(1, "  Proveedor    SA ", 5).obtener_nombre() == "Proveedor SA"


@pytest.mark.parametrize("plazo", [2.5, "5", None, True])
def test_proveedor_plazo_no_entero(plazo):
    with pytest.raises(PlazoDeEntregaNoEnteroError):
        Proveedor(1, "Proveedor SA", plazo)


@pytest.mark.parametrize("plazo", [0, -3])
def test_proveedor_plazo_no_positivo(plazo):
    with pytest.raises(PlazoDeEntregaNoPositivoError):
        Proveedor(1, "Proveedor SA", plazo)


def test_mail_y_telefono_son_opcionales():
    proveedor = Proveedor(1, "Proveedor SA", 5)

    assert proveedor.mail is None
    assert proveedor.telefono is None


@pytest.mark.parametrize("id_proveedor", [0, -2, "P1", None, 1.0])
def test_proveedor_id_invalido(id_proveedor):
    with pytest.raises(IdentificadorDeProveedorInvalidoError):
        Proveedor(id_proveedor, "Proveedor SA", 5)


def test_proveedor_id_duplicado():
    Proveedor.registrar_id(1)

    with pytest.raises(IdentificadorDeProveedorDuplicadoError):
        Proveedor(1, "Otro", 5)


@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_proveedor_nombre_invalido(nombre):
    with pytest.raises(NombreDeProveedorVacioError):
        Proveedor(1, nombre, 5)


@pytest.mark.parametrize("mail", ["sin-arroba", "a@b", "a @b.com", ""])
def test_proveedor_mail_invalido(mail):
    with pytest.raises(CorreoElectronicoInvalidoError):
        Proveedor(1, "Proveedor SA", 5, mail=mail)


@pytest.mark.parametrize("telefono", ["123", "telefono", ""])
def test_proveedor_telefono_invalido(telefono):
    with pytest.raises(NumeroDeTelefonoInvalidoError):
        Proveedor(1, "Proveedor SA", 5, telefono=telefono)


def test_agregar_pedido_pendiente():
    proveedor = Proveedor(1, "Proveedor SA", 5)
    pedido = crear_pedido(1, 1, 1)

    proveedor.agregar_pedido_pendiente(pedido)

    assert proveedor.obtener_pedidos_pendientes() == [pedido]


def test_agregar_pedido_pendiente_que_no_es_pedido():
    proveedor = Proveedor(1, "Proveedor SA", 5)

    with pytest.raises(ObjetoNoEsUnPedidoError):
        proveedor.agregar_pedido_pendiente("PED-1")


def test_agregar_pedido_de_otro_proveedor():
    proveedor = Proveedor(1, "Proveedor SA", 5)

    with pytest.raises(PedidoDeOtroProveedorError):
        proveedor.agregar_pedido_pendiente(crear_pedido(1, 2, 1))


def test_eliminar_pedido_pendiente():
    proveedor = Proveedor(1, "Proveedor SA", 5)
    p1 = crear_pedido(1, 1, 1)
    p2 = crear_pedido(2, 1, 2)
    proveedor.agregar_pedido_pendiente(p1)
    proveedor.agregar_pedido_pendiente(p2)

    proveedor.eliminar_pedido_pendiente(1)

    assert proveedor.obtener_pedidos_pendientes() == [p2]


def test_guardar_pedidos_pendientes_valida_y_copia():
    proveedor = Proveedor(1, "Proveedor SA", 5)
    pedidos = [crear_pedido(1, 1, 1)]

    proveedor.guardar_pedidos_pendientes(pedidos)
    pedidos.clear()

    assert len(proveedor.obtener_pedidos_pendientes()) == 1


def test_guardar_pedidos_pendientes_con_pedido_ajeno():
    proveedor = Proveedor(1, "Proveedor SA", 5)

    with pytest.raises(PedidoDeOtroProveedorError):
        proveedor.guardar_pedidos_pendientes([crear_pedido(1, 2, 1)])


def test_generar_remesa_devuelve_una_remesa():
    remesa = Proveedor.generar_remesa(1, "aluminio", 1, 1, 10, 100, fecha(), lote="L-1")

    assert isinstance(remesa, Remesa)
    assert remesa.obtener_saldo() == 10
    assert remesa.obtener_precio_unitario() == 100
    assert remesa.obtener_dato("lote") == "L-1"
