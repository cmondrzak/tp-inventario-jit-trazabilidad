import pytest

from proveedor import Proveedor
from exceptions import DatoInvalidoError, NombreInvalidoError


def test_creacion_proveedor_valida():
    proveedor = Proveedor("P1", "Proveedor SA", "contacto@proveedor.com", "+54 11 5555-5555")

    assert proveedor.id_proveedor == "P1"
    assert proveedor.nombre == "Proveedor SA"
    assert proveedor.mail == "contacto@proveedor.com"
    assert proveedor.telefono == "+54 11 5555-5555"


def test_proveedor_nombre_vacio_lanza_error():
    with pytest.raises(NombreInvalidoError):
        Proveedor("P1", "", "contacto@proveedor.com", "12345678")


def test_proveedor_nombre_none_lanza_error():
    with pytest.raises(NombreInvalidoError):
        Proveedor("P1", None, "contacto@proveedor.com", "12345678")


def test_proveedor_mail_invalido_lanza_error():
    with pytest.raises(DatoInvalidoError):
        Proveedor("P1", "Proveedor SA", "no-es-un-mail", "12345678")


def test_proveedor_telefono_invalido_lanza_error():
    with pytest.raises(DatoInvalidoError):
        Proveedor("P1", "Proveedor SA", "contacto@proveedor.com", "abc")