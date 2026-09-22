from datetime import date

import pytest

from remesa import Remesa
from exceptions import CantidadInvalidaError, SaldoInvalidoError


def crear_remesa(**overrides):
    datos = dict(
        id_remesa="R-1",
        material=None,
        proveedor=None,
        cantidad_recibida=10,
        fecha_recepcion=date(2026, 3, 2),
    )
    datos.update(overrides)
    return Remesa(**datos)


# ---------------------------------------------------------------------------
# Validaciones básicas
# ---------------------------------------------------------------------------

def test_creacion_remesa_valida():
    remesa = crear_remesa()

    assert remesa.cantidad_recibida == 10
    assert remesa.saldo_disponible == 10  # RN12


def test_remesa_cantidad_recibida_cero_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        crear_remesa(cantidad_recibida=0)


def test_remesa_cantidad_recibida_negativa_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        crear_remesa(cantidad_recibida=-5)


def test_remesa_cantidad_recibida_none_lanza_error():
    with pytest.raises(CantidadInvalidaError):
        crear_remesa(cantidad_recibida=None)


# ---------------------------------------------------------------------------
# **kwargs: datos opcionales (la consigna)
# ---------------------------------------------------------------------------

def test_remesa_sin_fecha_vencimiento_no_lanza_error():
    # RN13: una remesa puede no tener fecha de vencimiento.
    remesa = crear_remesa()
    assert remesa.fecha_vencimiento is None


def test_remesa_con_fecha_vencimiento_por_kwargs():
    remesa = crear_remesa(fecha_vencimiento=date(2026, 3, 20))
    assert remesa.fecha_vencimiento == date(2026, 3, 20)


def test_remesa_datos_opcionales_no_declarados_se_guardan_y_son_consultables():
    # Simula un campo futuro que el README anticipa (lote del
    # proveedor) sin que Remesa.__init__ tenga que declararlo.
    remesa = crear_remesa(lote_proveedor="L-998", temperatura_recepcion=4.5)

    assert remesa.obtener_dato("lote_proveedor") == "L-998"
    assert remesa.obtener_dato("temperatura_recepcion") == 4.5


def test_remesa_dato_opcional_no_provisto_devuelve_default():
    remesa = crear_remesa()
    assert remesa.obtener_dato("nro_guia") is None
    assert remesa.obtener_dato("nro_guia", "sin dato") == "sin dato"


def test_remesa_kwargs_no_pisan_atributos_obligatorios():
    # Los datos opcionales viven en su propio diccionario; no pueden
    # pisar cantidad_recibida ni ningún otro atributo "core".
    remesa = crear_remesa(cantidad_recibida=10, fecha_vencimiento=date(2026, 3, 20))
    assert remesa.cantidad_recibida == 10
    assert remesa.datos_opcionales == {"fecha_vencimiento": date(2026, 3, 20)}


# ---------------------------------------------------------------------------
# esta_vencida / es_utilizable (RN17)
# ---------------------------------------------------------------------------

def test_remesa_sin_vencimiento_nunca_esta_vencida():
    remesa = crear_remesa()
    assert remesa.esta_vencida(date(2099, 1, 1)) is False


def test_remesa_vencida_cuando_fecha_supera_vencimiento():
    remesa = crear_remesa(fecha_vencimiento=date(2026, 3, 20))
    assert remesa.esta_vencida(date(2026, 3, 21)) is True
    assert remesa.esta_vencida(date(2026, 3, 20)) is False


def test_remesa_utilizable_requiere_saldo_y_no_vencida():
    remesa = crear_remesa(fecha_vencimiento=date(2026, 3, 20))
    assert remesa.es_utilizable(date(2026, 3, 10)) is True

    remesa.consumir(10)  # agota el saldo
    assert remesa.es_utilizable(date(2026, 3, 10)) is False


# ---------------------------------------------------------------------------
# consumir (RN10, RN11, RN21)
# ---------------------------------------------------------------------------

def test_consumir_reduce_el_saldo():
    remesa = crear_remesa(cantidad_recibida=10)
    remesa.consumir(4)
    assert remesa.saldo_disponible == 6


def test_consumir_cantidad_mayor_al_saldo_lanza_error():
    remesa = crear_remesa(cantidad_recibida=10)
    with pytest.raises(SaldoInvalidoError):
        remesa.consumir(11)
    assert remesa.saldo_disponible == 10  # no se modifica en el error


def test_consumir_cantidad_no_positiva_lanza_error():
    remesa = crear_remesa(cantidad_recibida=10)
    with pytest.raises(CantidadInvalidaError):
        remesa.consumir(0)


def test_consumir_nunca_deja_saldo_negativo():
    remesa = crear_remesa(cantidad_recibida=5)
    remesa.consumir(5)
    assert remesa.saldo_disponible == 0
    with pytest.raises(SaldoInvalidoError):
        remesa.consumir(1)