import pytest

from validaciones import Validaciones
from exceptions import IdentificadorDuplicadoError


def test_es_positivo_valor_positivo_retorna_true():
    assert Validaciones.es_positivo(10) is True


def test_es_positivo_cero_retorna_false():
    assert Validaciones.es_positivo(0) is False


def test_es_positivo_negativo_retorna_false():
    assert Validaciones.es_positivo(-5) is False


def test_es_positivo_none_retorna_false():
    assert Validaciones.es_positivo(None) is False


def test_es_positivo_bool_no_se_confunde_con_entero():
    # bool es subclase de int en Python: True == 1. Sin el chequeo
    # explícito, es_positivo(True) daría True, lo cual no tiene
    # sentido como "cantidad" o "precio".
    assert Validaciones.es_positivo(True) is False


def test_es_no_negativo_cero_retorna_true():
    assert Validaciones.es_no_negativo(0) is True


def test_es_no_negativo_negativo_retorna_false():
    assert Validaciones.es_no_negativo(-1) is False


def test_es_no_vacio_texto_con_contenido_retorna_true():
    assert Validaciones.es_no_vacio("Aluminio") is True


def test_es_no_vacio_string_vacio_retorna_false():
    assert Validaciones.es_no_vacio("") is False


def test_es_no_vacio_solo_espacios_retorna_false():
    assert Validaciones.es_no_vacio("   ") is False


def test_es_no_vacio_none_retorna_false():
    assert Validaciones.es_no_vacio(None) is False


def test_validar_no_duplicado_id_libre_no_lanza_error():
    Validaciones.validar_no_duplicado(1, {})  # no debe lanzar


def test_validar_no_duplicado_id_usado_lanza_error():
    coleccion = {1: "algo"}
    with pytest.raises(IdentificadorDuplicadoError):
        Validaciones.validar_no_duplicado(1, coleccion)


def test_es_email_valido():
    assert Validaciones.es_email_valido("contacto@proveedor.com") is True
    assert Validaciones.es_email_valido("sin-arroba.com") is False
    assert Validaciones.es_email_valido(None) is False


def test_es_telefono_valido():
    assert Validaciones.es_telefono_valido("+54 11 5555-5555") is True
    assert Validaciones.es_telefono_valido("abc") is False