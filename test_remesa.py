from datetime import date

import pytest

from remesa import Remesa
from exceptions import CantidadInvalidaError, IdentificadorDuplicadoError, MaterialNoEncontradoError, ProveedorNoEncontradoError


@pytest.fixture(autouse=True)
def reset_remesa_state():
    Remesa.lista_id = []


def crear_remesa(**overrides):
    datos = dict(
        id_remesa="R-1",
        material="AL-01",
        proveedor="P1",
        renglon_pedido=None,
        cantidad_recibida=10,
        saldo_disponible=10,
    )
    datos.update(overrides)
    return Remesa(**datos)


def test_creacion_remesa_valida():
    remesa = crear_remesa()

    assert remesa.id_remesa == "R-1"
    assert remesa.cantidad_recibida == 10
    assert remesa.saldo_disponible == 10


def test_remesa_id_duplicado_lanza_error():
    crear_remesa(id_remesa="R-1")

    with pytest.raises(IdentificadorDuplicadoError):
        crear_remesa(id_remesa="R-1")


def test_remesa_material_vacio_lanza_error():
    with pytest.raises(MaterialNoEncontradoError):
        crear_remesa(material="")


def test_remesa_proveedor_vacio_lanza_error():
    with pytest.raises(ProveedorNoEncontradoError):
        crear_remesa(proveedor="")


def test_remesa_cantidad_recibida_cero_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        crear_remesa(cantidad_recibida=0)


def test_remesa_cantidad_recibida_negativa_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        crear_remesa(cantidad_recibida=-5)


def test_obtener_dato_con_dato_presente():
    remesa = crear_remesa(lote_proveedor="L-998")

    assert remesa.obtener_dato("lote_proveedor") == "L-998"


def test_obtener_dato_ausente_devuelve_default():
    remesa = crear_remesa()

    assert remesa.obtener_dato("nro_guia") is None
    assert remesa.obtener_dato("nro_guia", "sin dato") == "sin dato"


def test_obtener_fecha_vencimiento_ausente_es_none():
    remesa = crear_remesa()

    assert remesa.obtener_fecha_vencimiento() is None


def test_obtener_fecha_vencimiento_presente():
    remesa = crear_remesa(fecha_vencimiento=date(2026, 3, 20))

    assert remesa.obtener_fecha_vencimiento() == date(2026, 3, 20)


def test_consumir_reduce_el_saldo():
    remesa = crear_remesa(cantidad_recibida=10)

    remesa.consumir(4)

    assert remesa.saldo_disponible == 6


def test_consumir_cantidad_mayor_al_saldo_lanza_error():
    remesa = crear_remesa(cantidad_recibida=10)

    with pytest.raises(Exception):
        remesa.consumir(11)


def test_consumir_cantidad_no_positiva_lanza_error():
    remesa = crear_remesa(cantidad_recibida=10)

    with pytest.raises(CantidadInvalidaError):
        remesa.consumir(0)


def test_obtener_idremesa():
    remesa = crear_remesa(id_remesa="R-1")

    assert remesa.obtener_idremesa() == "R-1"


def test_esta_vencida_sin_fecha_de_vencimiento_nunca_esta_vencida():
    remesa = crear_remesa()

    assert remesa.esta_vencida(date(2026, 1, 1)) is False


def test_es_utilizable_con_saldo_y_sin_vencimiento_es_true():
    remesa = crear_remesa(cantidad_recibida=10)

    assert remesa.es_utilizable(date(2026, 1, 1)) is True


def test_obtener_material_devuelve_el_material():
    remesa = crear_remesa(material="AL-01")

    assert remesa.obtener_material() == "AL-01"


def test_obtener_cantidad_recibida_devuelve_la_cantidad():
    remesa = crear_remesa(cantidad_recibida=10)

    assert remesa.obtener_cantidad_recibida() == 10
