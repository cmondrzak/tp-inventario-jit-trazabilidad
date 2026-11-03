import pytest

from movimiento_retiro import Movimiento_retiro
from renglon_retiro import RenglonRetiro
from deposito import Deposito
from material import Material
from remesa import Remesa
from conftest import fecha
from exceptions import (
    IdentificadorDeMovimientoInvalidoError,
    IdentificadorDeMovimientoDuplicadoError,
    FormatoDeFechaInvalidoError,
    FechaDeRetiroFuturaError,
    RenglonesDelRetiroNoSonUnaListaError,
    RetiroSinRenglonesError,
    ElementoNoEsUnRenglonDeRetiroError,
    MaterialRepetidoEnElRetiroError,
    MaterialNoRegistradoError,
    MaterialNoIndicadoError,
    MaterialInvalidoError,
    CantidadARetirarNoPositivaError,
    ExistenciaDisponibleInsuficienteParaElRetiroError,
    RetiroYaRealizadoError,
)


@pytest.fixture
def deposito():
    """Aluminio: remesa 1 (5, vence en 3 dias) y remesa 2 (10, vence en 30). Titanio: remesa 3 (8)."""
    d = Deposito({}, {})
    d.modificar_materiales(Material(1, "aluminio", "kg", 10), 1)
    d.modificar_materiales(Material(2, "titanio", "kg", 5), 2)
    d.almacenar_remesa(Remesa(1, "aluminio", 1, 1, 5, fecha(-5), fecha_vencimiento=fecha(3)))
    d.almacenar_remesa(Remesa(2, "aluminio", 1, 2, 10, fecha(-5), fecha_vencimiento=fecha(30)))
    d.almacenar_remesa(Remesa(3, "titanio", 1, 3, 8, fecha(-5)))
    return d


def crear_retiro(deposito, renglones, id_mov=1, fecha_retiro=None):
    return Movimiento_retiro(id_mov, fecha_retiro or fecha(), renglones, deposito, deposito.retirar_fefo)


def plan(retiro):
    return [(r.obtener_id_remesa(), c) for r, c in retiro.obtener_remesas_modificadas()]


# --- ingreso de datos -------------------------------------------------------

def test_creacion_retiro_valido_planifica_sin_consumir(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 8)])

    assert retiro.obtener_id_movimiento() == 1
    assert retiro.obtener_estado() == "no retirado"
    assert plan(retiro) == [(1, 5), (2, 3)]
    assert deposito.obtener_remesa(1).obtener_saldo() == 5


@pytest.mark.parametrize("id_mov", [0, -1, "M1", None])
def test_id_invalido(deposito, id_mov):
    with pytest.raises(IdentificadorDeMovimientoInvalidoError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 1)], id_mov=id_mov)


def test_id_duplicado(deposito):
    Movimiento_retiro.registrar_id(1)

    with pytest.raises(IdentificadorDeMovimientoDuplicadoError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 1)])


@pytest.mark.parametrize("valor", ["2026-01-01", "", "40/01/2026", None])
def test_fecha_formato_invalido(deposito, valor):
    with pytest.raises(FormatoDeFechaInvalidoError):
        Movimiento_retiro(1, valor, [RenglonRetiro("aluminio", 1)], deposito, deposito.retirar_fefo)


def test_fecha_futura(deposito):
    with pytest.raises(FechaDeRetiroFuturaError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 1)], fecha_retiro=fecha(1))


@pytest.mark.parametrize("renglones", [None, "aluminio", (RenglonRetiro("aluminio", 1),)])
def test_renglones_no_son_lista(deposito, renglones):
    with pytest.raises(RenglonesDelRetiroNoSonUnaListaError):
        crear_retiro(deposito, renglones)


def test_retiro_sin_renglones(deposito):
    with pytest.raises(RetiroSinRenglonesError):
        crear_retiro(deposito, [])


def test_elemento_no_es_renglon(deposito):
    with pytest.raises(ElementoNoEsUnRenglonDeRetiroError):
        crear_retiro(deposito, [("aluminio", 3)])


def test_material_repetido_normalizado(deposito):
    with pytest.raises(MaterialRepetidoEnElRetiroError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 1), RenglonRetiro(" ALUMINIO ", 1)])


def test_material_no_registrado(deposito):
    with pytest.raises(MaterialNoRegistradoError):
        crear_retiro(deposito, [RenglonRetiro("cobre", 1)])


def test_existencia_insuficiente(deposito):
    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 16)])


def test_no_usa_remesas_vencidas_a_la_fecha_del_retiro(deposito):
    deposito.almacenar_remesa(Remesa(4, "aluminio", 1, 4, 50, fecha(-10), fecha_vencimiento=fecha(-1)))

    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        crear_retiro(deposito, [RenglonRetiro("aluminio", 16)])


def test_material_con_mayusculas_se_normaliza(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("  Aluminio ", 2)])

    assert plan(retiro) == [(1, 2)]


# --- confirmar el retiro ----------------------------------------------------

def test_cambiar_estado_consume_en_orden_fefo(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 8), RenglonRetiro("titanio", 2)])

    retiro.cambiar_estado()

    assert retiro.obtener_estado() == "retirado"
    assert plan(retiro) == [(1, 5), (2, 3), (3, 2)]
    assert deposito.obtener_remesa(2).obtener_saldo() == 7
    assert deposito.obtener_remesa(3).obtener_saldo() == 6
    assert "1" in deposito.obtener_remesas_agotadas()
    assert "1" not in deposito.obtener_remesas()


def test_cambiar_estado_dos_veces(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 1)])
    retiro.cambiar_estado()

    with pytest.raises(RetiroYaRealizadoError):
        retiro.cambiar_estado()


def test_cambiar_estado_replanifica_si_cambio_el_stock(deposito):
    r1 = crear_retiro(deposito, [RenglonRetiro("aluminio", 10)], id_mov=1)
    r2 = crear_retiro(deposito, [RenglonRetiro("aluminio", 10)], id_mov=2)
    r1.cambiar_estado()

    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        r2.cambiar_estado()
    assert r2.obtener_estado() == "no retirado"
    assert deposito.obtener_remesa(2).obtener_saldo() == 5


def test_cambiar_estado_con_material_en_mayusculas(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("Aluminio", 2)])

    retiro.cambiar_estado()

    assert deposito.obtener_remesa(1).obtener_saldo() == 3


def test_cambiar_estado_no_consume_nada_si_un_renglon_falla(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 3), RenglonRetiro("titanio", 8)])
    deposito.obtener_remesa(3).consumir(1)

    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        retiro.cambiar_estado()
    assert deposito.obtener_remesa(1).obtener_saldo() == 5


# --- edicion de renglones ---------------------------------------------------

def test_agregar_renglon(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    retiro.agregar_renglon("Titanio", 3)

    assert [r.obtener_material() for r in retiro.obtener_renglones()] == ["aluminio", "titanio"]
    assert plan(retiro) == [(1, 2), (3, 3)]


def test_agregar_renglon_material_repetido(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    with pytest.raises(MaterialRepetidoEnElRetiroError):
        retiro.agregar_renglon(" ALUMINIO", 1)


def test_agregar_renglon_cantidad_invalida(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    with pytest.raises(CantidadARetirarNoPositivaError):
        retiro.agregar_renglon("titanio", 0)


@pytest.mark.parametrize("material", [None, 5])
def test_agregar_renglon_material_no_texto(deposito, material):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    with pytest.raises(MaterialNoIndicadoError):
        retiro.agregar_renglon(material, 1)


def test_agregar_renglon_sin_stock_no_modifica_el_retiro(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    with pytest.raises(ExistenciaDisponibleInsuficienteParaElRetiroError):
        retiro.agregar_renglon("titanio", 100)
    assert len(retiro.obtener_renglones()) == 1


def test_agregar_renglon_a_retiro_realizado(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])
    retiro.cambiar_estado()

    with pytest.raises(RetiroYaRealizadoError):
        retiro.agregar_renglon("titanio", 1)


def test_eliminar_renglon(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2), RenglonRetiro("titanio", 1)])

    retiro.eliminar_renglon(" Aluminio")

    assert [r.obtener_material() for r in retiro.obtener_renglones()] == ["titanio"]
    assert plan(retiro) == [(3, 1)]


def test_eliminar_unico_renglon(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2)])

    with pytest.raises(RetiroSinRenglonesError):
        retiro.eliminar_renglon("aluminio")


def test_eliminar_renglon_inexistente(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2), RenglonRetiro("titanio", 1)])

    with pytest.raises(MaterialInvalidoError):
        retiro.eliminar_renglon("cobre")


@pytest.mark.parametrize("material", ["", None])
def test_eliminar_renglon_sin_material(deposito, material):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2), RenglonRetiro("titanio", 1)])

    with pytest.raises(MaterialNoIndicadoError):
        retiro.eliminar_renglon(material)


def test_eliminar_renglon_y_volver_a_agregarlo(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2), RenglonRetiro("titanio", 1)])

    retiro.eliminar_renglon("titanio")
    retiro.agregar_renglon("titanio", 4)

    assert plan(retiro) == [(1, 2), (3, 4)]


def test_eliminar_renglon_de_retiro_realizado(deposito):
    retiro = crear_retiro(deposito, [RenglonRetiro("aluminio", 2), RenglonRetiro("titanio", 1)])
    retiro.cambiar_estado()

    with pytest.raises(RetiroYaRealizadoError):
        retiro.eliminar_renglon("titanio")
