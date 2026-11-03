import pytest

from material import Material
from exceptions import (
    IdentificadorDeMaterialInvalidoError,
    IdentificadorDeMaterialDuplicadoError,
    NombreDeMaterialVacioError,
    UnidadDeMedidaVaciaError,
    PuntoDeReposicionNoEnteroError,
    PuntoDeReposicionNoPositivoError,
    ExistenciaDisponibleInvalidaError,
)


def test_creacion_material_valida():
    material = Material(1, "Aluminio", "kg", 10)

    assert material.id_material == 1
    assert material.obtener_nombre() == "Aluminio"
    assert material.obtener_unidad() == "kg"
    assert material.obtener_punto_reposicion() == 10


@pytest.mark.parametrize("id_material", [0, -1, "AL-01", 1.5, None, True])
def test_material_id_invalido(id_material):
    with pytest.raises(IdentificadorDeMaterialInvalidoError):
        Material(id_material, "Aluminio", "kg", 10)


def test_material_id_duplicado():
    Material.registrar_id(1)

    with pytest.raises(IdentificadorDeMaterialDuplicadoError):
        Material(1, "Otro", "kg", 5)


@pytest.mark.parametrize("nombre", ["", "   ", None, 5])
def test_material_nombre_invalido(nombre):
    with pytest.raises(NombreDeMaterialVacioError):
        Material(1, nombre, "kg", 10)


@pytest.mark.parametrize("unidad", ["", "  ", None, 1])
def test_material_unidad_invalida(unidad):
    with pytest.raises(UnidadDeMedidaVaciaError):
        Material(1, "Aluminio", unidad, 10)


@pytest.mark.parametrize("punto", [2.5, "10", None, True])
def test_material_punto_reposicion_no_entero(punto):
    with pytest.raises(PuntoDeReposicionNoEnteroError):
        Material(1, "Aluminio", "kg", punto)


@pytest.mark.parametrize("punto", [0, -5])
def test_material_punto_reposicion_no_positivo(punto):
    with pytest.raises(PuntoDeReposicionNoPositivoError):
        Material(1, "Aluminio", "kg", punto)


def test_crear_material_no_registra_el_id():
    Material(1, "Aluminio", "kg", 10)

    assert Material.obtener_lista_id() == []


@pytest.mark.parametrize("existencia, esperado", [(0, True), (9, True), (10, False), (50, False)])
def test_requiere_reposicion(existencia, esperado):
    material = Material(1, "Aluminio", "kg", 10)

    assert material.requiere_reposicion(existencia) is esperado


@pytest.mark.parametrize("existencia", [-1, "5", None])
def test_requiere_reposicion_existencia_invalida(existencia):
    material = Material(1, "Aluminio", "kg", 10)

    with pytest.raises(ExistenciaDisponibleInvalidaError):
        material.requiere_reposicion(existencia)


def test_guardar_lista_id():
    Material.guardar_lista_id([1, 2])

    assert Material.obtener_lista_id() == [1, 2]
