import pytest

from material import Material
from exceptions import NombreInvalidoError, PuntoDeReposicionInvalidoError


def test_creacion_material_valida():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert material.id_material == "AL-01"
    assert material.nombre == "Aluminio AL-01"
    assert material.unidad == "kg"
    assert material.punto_reposicion == 10


def test_material_nombre_vacio_lanza_error():
    with pytest.raises(NombreInvalidoError, match="El nombre no puede estar vacío"):
        Material("AL-01", "", "kg", 10)


def test_material_nombre_solo_espacios_lanza_error():
    with pytest.raises(NombreInvalidoError, match="El nombre no puede estar vacío"):
        Material("AL-01", "   ", "kg", 10)


def test_material_nombre_none_lanza_error():
    with pytest.raises(NombreInvalidoError, match="El nombre no puede estar vacío"):
        Material("AL-01", None, "kg", 10)


def test_material_unidad_vacia_lanza_error():
    with pytest.raises(NombreInvalidoError, match="unidad de medida"):
        Material("AL-01", "Aluminio AL-01", "", 10)


def test_material_punto_reposicion_cero_lanza_error():
    with pytest.raises(PuntoDeReposicionInvalidoError, match="El punto de reposición debe ser mayor que cero"):
        Material("AL-01", "Aluminio AL-01", "kg", 0)


def test_material_punto_reposicion_negativo_lanza_error():
    with pytest.raises(PuntoDeReposicionInvalidoError):
        Material("AL-01", "Aluminio AL-01", "kg", -5)


def test_material_punto_reposicion_none_lanza_error():
    with pytest.raises(PuntoDeReposicionInvalidoError):
        Material("AL-01", "Aluminio AL-01", "kg", None)


def test_requiere_reposicion_por_debajo_del_punto():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)
    assert material.requiere_reposicion(9) is True


def test_no_requiere_reposicion_en_o_por_encima_del_punto():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)
    assert material.requiere_reposicion(10) is False
    assert material.requiere_reposicion(11) is False