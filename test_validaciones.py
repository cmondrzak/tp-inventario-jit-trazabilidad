import pytest

from validaciones import Validaciones


def test_es_numero_entero_es_true():
    assert Validaciones.es_numero(10) is True


def test_es_numero_bool_no_cuenta_como_numero():
    assert not Validaciones.es_numero(True)


def test_es_numero_string_no_es_numero():
    assert not Validaciones.es_numero("10")


def test_es_positivo_valor_positivo():
    assert Validaciones.es_positivo(10)


def test_es_positivo_cero_es_false():
    assert not Validaciones.es_positivo(0)


def test_es_positivo_negativo_es_false():
    assert not Validaciones.es_positivo(-5)


def test_es_no_negativo_cero_es_true():
    assert Validaciones.es_no_negativo(0)


def test_es_no_negativo_negativo_es_false():
    assert not Validaciones.es_no_negativo(-1)


def test_es_no_vacio_texto_con_contenido():
    assert Validaciones.es_no_vacio("Aluminio")


def test_es_no_vacio_string_vacio_es_false():
    assert not Validaciones.es_no_vacio("")


def test_es_no_vacio_solo_espacios_es_false():
    assert not Validaciones.es_no_vacio("   ")


def test_es_no_vacio_none_es_false():
    assert not Validaciones.es_no_vacio(None)


def test_validarid_id_libre_devuelve_true():
    assert Validaciones.validarid([], "AL-01") is True


def test_validarid_id_usado_devuelve_false():
    assert Validaciones.validarid(["AL-01"], "AL-01") is False


def test_es_fecha_con_date_es_true():
    from datetime import date
    assert Validaciones.es_fecha(date(2026, 3, 1))


def test_es_fecha_con_string_es_false():
    assert not Validaciones.es_fecha("2026-03-01")
