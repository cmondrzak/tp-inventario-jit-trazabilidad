from datetime import date

import pytest

from validaciones import Validaciones


@pytest.mark.parametrize("valor", [10, 0, -3, 2.5])
def test_es_numero_acepta_int_y_float(valor):
    assert Validaciones.es_numero(valor) is True


@pytest.mark.parametrize("valor", [True, False, "10", None, [1]])
def test_es_numero_rechaza_bool_texto_y_otros(valor):
    assert Validaciones.es_numero(valor) is False


def test_es_numero_entero():
    assert Validaciones.es_numero_entero(5)
    assert not Validaciones.es_numero_entero(5.0)
    assert not Validaciones.es_numero_entero(True)
    assert not Validaciones.es_numero_entero("5")


@pytest.mark.parametrize("valor, esperado", [(1, True), (100, True), (0, False), (-1, False), (1.0, False), (True, False), ("1", False), (None, False)])
def test_es_identificador_valido(valor, esperado):
    assert Validaciones.es_identificador_valido(valor) is esperado


@pytest.mark.parametrize("valor, esperado", [(10, True), (0.5, True), (0, False), (-5, False), ("3", False), (None, False)])
def test_es_positivo(valor, esperado):
    assert Validaciones.es_positivo(valor) is esperado


@pytest.mark.parametrize("valor, esperado", [(0, True), (3, True), (-1, False), ("0", False)])
def test_es_no_negativo(valor, esperado):
    assert Validaciones.es_no_negativo(valor) is esperado


@pytest.mark.parametrize("valor, esperado", [("Aluminio", True), ("", False), ("   ", False), (None, False), ([], False), ([1], True), ({}, False), ({"a": 1}, True), (0, True)])
def test_es_no_vacio(valor, esperado):
    assert Validaciones.es_no_vacio(valor) is esperado


@pytest.mark.parametrize("valor, esperado", [("kg", True), ("  kg  ", True), ("", False), ("   ", False), (None, False), (5, False)])
def test_es_texto_no_vacio(valor, esperado):
    assert Validaciones.es_texto_no_vacio(valor) is esperado


def test_normalizar_texto_saca_espacios_y_pasa_a_minuscula():
    assert Validaciones.normalizar_texto("  Aluminio   AL-01 ") == "aluminio al-01"


def test_validarid():
    assert Validaciones.validarid([], 1) is True
    assert Validaciones.validarid([1, 2], 3) is True
    assert Validaciones.validarid([1, 2], 2) is False


@pytest.mark.parametrize("texto", ["01/03/2026", " 29/02/2024 ", "31/12/1999"])
def test_es_fecha_valida(texto):
    assert Validaciones.es_fecha(texto) is True


@pytest.mark.parametrize("texto", ["2026-03-01", "1/3/2026", "29/02/2025", "32/01/2026", "01/13/2026", "", "hoy", None, date(2026, 3, 1)])
def test_es_fecha_invalida(texto):
    assert Validaciones.es_fecha(texto) is False


@pytest.mark.parametrize("mail", ["a@b.com", "contacto@proveedor.com.ar", "nombre.apellido@empresa.io"])
def test_es_mail_valido(mail):
    assert Validaciones.es_mail_valido(mail) is True


@pytest.mark.parametrize("mail", ["", "sinarroba.com", "a@@b.com", "a@b@c.com", "@b.com", "a@", "a@com", "a@.com", "a@b.", "a@b..com", "a b@c.com", None, 123])
def test_es_mail_invalido(mail):
    assert Validaciones.es_mail_valido(mail) is False


@pytest.mark.parametrize("telefono", ["12345678", "11 1234-5678", "+54 11 1234 5678", " +5491112345678 "])
def test_es_telefono_valido(telefono):
    assert Validaciones.es_telefono_valido(telefono) is True


@pytest.mark.parametrize("telefono", ["1234567", "abc12345678", "", "11.1234.5678", 12345678, None,
                                      "+1+2+3+4+5+6+7+8", "54+1112345678", "++5411123456", "+", "--------"])
def test_es_telefono_invalido(telefono):
    assert Validaciones.es_telefono_valido(telefono) is False
