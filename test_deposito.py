import pytest

from deposito import Deposito
from remesa import Remesa
from material import Material
from conftest import fecha
from exceptions import (
    ObjetoNoEsUnaRemesaError,
    ObjetoNoEsUnMaterialError,
    IdentificadorDeRemesaDuplicadoError,
    IdentificadorDeMaterialDuplicadoError,
    IdentificadorDeMaterialNoCoincideConLaClaveError,
    MaterialNoRegistradoError,
    ExistenciaDisponibleInsuficienteParaElRetiroError,
)


def remesa(id_remesa, cantidad=10, material="aluminio", **datos):
    return Remesa(id_remesa, material, 1, 1, cantidad, datos.pop("fecha_recepcion", fecha(-5)), **datos)


@pytest.fixture
def deposito():
    d = Deposito({}, {})
    d.modificar_materiales(Material(1, "Aluminio", "kg", 10), 1)
    return d


# --- materiales -------------------------------------------------------------

def test_modificar_materiales_registra_el_material_y_su_id(deposito):
    assert isinstance(deposito.obtener_materiales()[1], Material)
    assert Material.obtener_lista_id() == [1]


def test_modificar_materiales_con_objeto_que_no_es_material(deposito):
    with pytest.raises(ObjetoNoEsUnMaterialError):
        deposito.modificar_materiales("aluminio", 2)


def test_modificar_materiales_con_clave_distinta(deposito):
    with pytest.raises(IdentificadorDeMaterialNoCoincideConLaClaveError):
        deposito.modificar_materiales(Material(2, "Titanio", "kg", 5), 3)


def test_modificar_materiales_con_id_repetido(deposito):
    material = Material(2, "Titanio", "kg", 5)
    material.id_material = 1

    with pytest.raises(IdentificadorDeMaterialDuplicadoError):
        deposito.modificar_materiales(material, 1)


def test_obtener_materiales_devuelve_copia(deposito):
    deposito.obtener_materiales().clear()

    assert 1 in deposito.obtener_materiales()


@pytest.mark.parametrize("nombre", ["Aluminio", "  aluminio ", "ALUMINIO"])
def test_material_registrado_normaliza(deposito, nombre):
    assert deposito.material_registrado(nombre) is True


def test_material_no_registrado(deposito):
    assert deposito.material_registrado("titanio") is False
    with pytest.raises(MaterialNoRegistradoError):
        deposito.validar_material_registrado("titanio")


# --- remesas ----------------------------------------------------------------

def test_almacenar_remesa(deposito):
    r = remesa(1)

    deposito.almacenar_remesa(r)

    assert deposito.obtener_remesas() == {"1": r}
    assert deposito.obtener_remesa(1) is r
    assert Remesa.obtener_lista_id() == [1]


def test_almacenar_algo_que_no_es_remesa(deposito):
    with pytest.raises(ObjetoNoEsUnaRemesaError):
        deposito.almacenar_remesa({"id": 1})


def test_almacenar_remesa_duplicada(deposito):
    deposito.almacenar_remesa(remesa(1))
    Remesa.lista_id = []

    with pytest.raises(IdentificadorDeRemesaDuplicadoError):
        deposito.almacenar_remesa(remesa(1))


def test_almacenar_remesa_agotada_va_a_agotadas(deposito):
    r = remesa(1, cantidad=5)
    r.consumir(5)

    deposito.almacenar_remesa(r)

    assert deposito.obtener_remesas() == {}
    assert deposito.obtener_remesas_agotadas() == {"1": r}
    assert deposito.obtener_remesa(1) is r


def test_obtener_remesa_inexistente(deposito):
    with pytest.raises(KeyError):
        deposito.obtener_remesa(99)


def test_archivar_remesa_agotada(deposito):
    r = remesa(1, cantidad=5)
    deposito.almacenar_remesa(r)
    r.consumir(5)

    deposito.archivar_remesa_agotada(r)

    assert deposito.obtener_remesas() == {}
    assert deposito.obtener_todas_las_remesas() == {"1": r}


def test_archivar_remesa_con_saldo_no_hace_nada(deposito):
    r = remesa(1, cantidad=5)
    deposito.almacenar_remesa(r)

    deposito.archivar_remesa_agotada(r)

    assert deposito.obtener_remesas() == {"1": r}


def test_actualizar_remesas_guardadas_mueve_las_agotadas(deposito):
    r1, r2 = remesa(1, cantidad=5), remesa(2, cantidad=5)
    deposito.almacenar_remesa(r1)
    deposito.almacenar_remesa(r2)
    r1.consumir(5)

    deposito.actualizar_remesas_guardadas()

    assert list(deposito.obtener_remesas()) == ["2"]
    assert list(deposito.obtener_remesas_agotadas()) == ["1"]


# --- existencia y reposicion ------------------------------------------------

def test_existencia_disponible_suma_solo_remesas_utilizables(deposito):
    deposito.almacenar_remesa(remesa(1, 10))
    deposito.almacenar_remesa(remesa(2, 7, fecha_vencimiento=fecha(10)))
    deposito.almacenar_remesa(remesa(3, 100, fecha_recepcion=fecha(-10), fecha_vencimiento=fecha(-1)))
    deposito.almacenar_remesa(remesa(4, 50, material="titanio"))

    assert deposito.existencia_disponible("aluminio") == 17


def test_existencia_disponible_con_remesa_en_mayusculas(deposito):
    deposito.almacenar_remesa(remesa(1, 10, material="Aluminio"))

    assert deposito.existencia_disponible("Aluminio") == 10


def test_remesas_por_material(deposito):
    r1 = remesa(1, 10)
    deposito.almacenar_remesa(r1)
    deposito.almacenar_remesa(remesa(2, 10, material="titanio"))

    assert deposito.remesas_por_material("aluminio", fecha()) == [r1]
    assert deposito.remesas_por_material("aluminio", fecha(-6)) == []


def test_validar_existencia_para_retiro(deposito):
    deposito.almacenar_remesa(remesa(1, 10))

    deposito.validar_existencia_para_retiro("aluminio", 10, fecha())
    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        deposito.validar_existencia_para_retiro("aluminio", 11, fecha())


def test_retirar_fefo():
    sin_vto = remesa(1)
    pronto = remesa(2, fecha_vencimiento=fecha(3))
    tarde = remesa(3, fecha_vencimiento=fecha(30))

    ordenadas = Deposito.retirar_fefo([sin_vto, tarde, pronto])

    assert ordenadas == [pronto, tarde, sin_vto]


def test_datos_reposicion(deposito):
    deposito.almacenar_remesa(remesa(1, 4))

    datos = deposito.obtener_datos_reposicion(1)

    assert datos == {
        "id_material": 1,
        "nombre": "Aluminio",
        "unidad": "kg",
        "existencia": 4,
        "punto_reposicion": 10,
        "diferencia": -6,
        "requiere_reposicion": True,
    }


def test_materiales_a_reponer(deposito):
    deposito.modificar_materiales(Material(2, "titanio", "kg", 5), 2)
    deposito.almacenar_remesa(remesa(1, 20, material="aluminio"))

    a_reponer = deposito.obtener_materiales_a_reponer()

    assert [d["id_material"] for d in a_reponer] == [2]
