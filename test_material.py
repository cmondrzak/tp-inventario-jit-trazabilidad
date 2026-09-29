import pytest

from material import Material
from exceptions import (
    IdentificadorDuplicadoError,
    NombreInvalidoError,
    PuntoDeReposicionInvalidoError,
    UnidadNoEncontradaError,
)


@pytest.fixture(autouse=True)
def reset_material_state():
    Material.lista_id = []


def test_creacion_material_valida():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert material.id_material == "AL-01"
    assert material.nombre == "Aluminio AL-01"
    assert material.unidad == "kg"
    assert material.punto_reposicion == 10


def test_material_id_vacio_lanza_error():
    with pytest.raises(NombreInvalidoError, match="identificador"):
        Material("", "Aluminio AL-01", "kg", 10)


def test_material_id_duplicado_lanza_error():
    Material("AL-01", "Aluminio AL-01", "kg", 10)

    with pytest.raises(IdentificadorDuplicadoError):
        Material("AL-01", "Otro material", "kg", 5)


def test_material_nombre_vacio_lanza_error():
    with pytest.raises(NombreInvalidoError, match="nombre"):
        Material("AL-01", "", "kg", 10)


def test_material_unidad_vacia_lanza_error():
    with pytest.raises(UnidadNoEncontradaError, match="unidad"):
        Material("AL-01", "Aluminio AL-01", "", 10)


def test_material_punto_reposicion_cero_lanza_error():
    with pytest.raises(PuntoDeReposicionInvalidoError, match="reposición"):
        Material("AL-01", "Aluminio AL-01", "kg", 0)


def test_material_punto_reposicion_negativo_lanza_error():
    with pytest.raises(PuntoDeReposicionInvalidoError, match="reposición"):
        Material("AL-01", "Aluminio AL-01", "kg", -5)
