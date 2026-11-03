from datetime import date, datetime, timedelta

import pytest

from remesa import Remesa
from conftest import fecha
from exceptions import (
    IdentificadorDeRemesaInvalidoError,
    IdentificadorDeRemesaDuplicadoError,
    MaterialNoIndicadoError,
    IdentificadorDeProveedorInvalidoError,
    RenglonDePedidoNoIndicadoError,
    CantidadRecibidaNoPositivaError,
    CantidadRecibidaNoEnteraError,
    PrecioInvalidoError,
    PrecioUnitarioNoPositivoError,
    PrecioUnitarioNoFinitoError,
    CantidadAConsumirNoPositivaError,
    FormatoDeFechaInvalidoError,
    FechaDeRecepcionFuturaError,
    FechaDeVencimientoAnteriorALaRecepcionError,
    FechaDeVencimientoPasadaError,
    SaldoDeRemesaInsuficienteError,
)


def crear_remesa(**cambios):
    datos = dict(
        id_remesa=1,
        material="aluminio",
        id_proveedor=1,
        id_renglon_pedido=1,
        cantidad_recibida=10,
        precio_unitario=50,
        fecha_recepcion=fecha(-5),
    )
    datos.update(cambios)
    return Remesa(**datos)


# --- ingreso de datos -------------------------------------------------------

def test_creacion_remesa_valida():
    remesa = crear_remesa(fecha_vencimiento=fecha(30), lote="L-998")

    assert remesa.obtener_id_remesa() == 1
    assert remesa.obtener_material() == "aluminio"
    assert remesa.obtener_id_proveedor() == 1
    assert remesa.obtener_id_renglon_pedido() == 1
    assert remesa.obtener_cantidad_recibida() == 10
    assert remesa.obtener_saldo() == 10
    assert remesa.obtener_precio_unitario() == 50
    assert remesa.costo_total() == 500
    assert remesa.obtener_fecha_recepcion() == fecha(-5)
    assert remesa.obtener_fecha_vencimiento() == fecha(30)
    assert remesa.obtener_dato("lote") == "L-998"
    assert remesa.obtener_dato("nro_guia") is None


@pytest.mark.parametrize("precio", [0, -1, "50", None])
def test_precio_unitario_invalido(precio):
    with pytest.raises(PrecioUnitarioNoPositivoError):
        crear_remesa(precio_unitario=precio)


def test_precio_unitario_decimal_y_costo_total():
    remesa = crear_remesa(cantidad_recibida=4, precio_unitario=12.5)

    assert remesa.costo_total() == 50


def test_costo_total_no_cambia_al_consumir():
    remesa = crear_remesa(cantidad_recibida=10, precio_unitario=3)
    remesa.consumir(4)

    assert remesa.costo_total() == 30


@pytest.mark.parametrize("id_remesa", [0, -1, "R-1", None])
def test_id_invalido(id_remesa):
    with pytest.raises(IdentificadorDeRemesaInvalidoError):
        crear_remesa(id_remesa=id_remesa)


def test_id_duplicado():
    Remesa.registrar_id(1)

    with pytest.raises(IdentificadorDeRemesaDuplicadoError):
        crear_remesa(id_remesa=1)


@pytest.mark.parametrize("material", ["", "  ", None])
def test_material_invalido(material):
    with pytest.raises(MaterialNoIndicadoError):
        crear_remesa(material=material)


@pytest.mark.parametrize("id_proveedor", [0, None, "P1"])
def test_proveedor_invalido(id_proveedor):
    with pytest.raises(IdentificadorDeProveedorInvalidoError):
        crear_remesa(id_proveedor=id_proveedor)


@pytest.mark.parametrize("id_renglon", [0, None, "R1"])
def test_renglon_pedido_invalido(id_renglon):
    with pytest.raises(RenglonDePedidoNoIndicadoError):
        crear_remesa(id_renglon_pedido=id_renglon)


@pytest.mark.parametrize("cantidad", [0, -5])
def test_cantidad_recibida_no_positiva(cantidad):
    with pytest.raises(CantidadRecibidaNoPositivaError):
        crear_remesa(cantidad_recibida=cantidad)


@pytest.mark.parametrize("cantidad", [2.5, "10", None, True])
def test_cantidad_recibida_no_entera(cantidad):
    with pytest.raises(CantidadRecibidaNoEnteraError):
        crear_remesa(cantidad_recibida=cantidad)


@pytest.mark.parametrize("precio", [float("inf"), float("1e309")])
def test_precio_unitario_infinito(precio):
    with pytest.raises(PrecioUnitarioNoFinitoError):
        crear_remesa(precio_unitario=precio)


def test_precio_unitario_nan():
    with pytest.raises(PrecioInvalidoError):
        crear_remesa(precio_unitario=float("nan"))


@pytest.mark.parametrize("valor", ["2026-03-01", "", None, "30/02/2026", date.today()])
def test_fecha_recepcion_formato_invalido(valor):
    with pytest.raises(FormatoDeFechaInvalidoError):
        crear_remesa(fecha_recepcion=valor)


def test_fecha_recepcion_futura():
    with pytest.raises(FechaDeRecepcionFuturaError):
        crear_remesa(fecha_recepcion=fecha(1))


def test_fecha_recepcion_hoy_es_valida():
    assert crear_remesa(fecha_recepcion=fecha()).obtener_fecha_recepcion() == fecha()


@pytest.mark.parametrize("valor", ["2026-03-01", "", "99/99/9999"])
def test_fecha_vencimiento_formato_invalido(valor):
    with pytest.raises(FormatoDeFechaInvalidoError):
        crear_remesa(fecha_vencimiento=valor)


def test_vencimiento_anterior_a_la_recepcion():
    with pytest.raises(FechaDeVencimientoAnteriorALaRecepcionError):
        crear_remesa(fecha_recepcion=fecha(-5), fecha_vencimiento=fecha(-6))


def test_vencimiento_igual_a_la_recepcion_es_valido():
    crear_remesa(fecha_recepcion=fecha(-5), fecha_vencimiento=fecha(-5))


@pytest.mark.parametrize("vencimiento", [None, fecha(), fecha(1), fecha(365)])
def test_vencimiento_no_pasado_acepta_hoy_futuro_o_sin_vencimiento(vencimiento):
    Remesa.validar_vencimiento_no_pasado(vencimiento)


@pytest.mark.parametrize("vencimiento", [fecha(-1), fecha(-30)])
def test_vencimiento_pasado(vencimiento):
    with pytest.raises(FechaDeVencimientoPasadaError):
        Remesa.validar_vencimiento_no_pasado(vencimiento)


def test_vencimiento_no_pasado_formato_invalido():
    with pytest.raises(FormatoDeFechaInvalidoError):
        Remesa.validar_vencimiento_no_pasado("2026-01-01")


def test_crear_remesa_no_registra_el_id():
    crear_remesa()

    assert Remesa.obtener_lista_id() == []


# --- consumo ----------------------------------------------------------------

def test_consumir_reduce_el_saldo():
    remesa = crear_remesa(cantidad_recibida=10)

    remesa.consumir(4)
    remesa.consumir(6)

    assert remesa.obtener_saldo() == 0
    assert remesa.obtener_cantidad_recibida() == 10


def test_consumir_mas_que_el_saldo():
    remesa = crear_remesa(cantidad_recibida=10)

    with pytest.raises(SaldoDeRemesaInsuficienteError):
        remesa.consumir(11)
    assert remesa.obtener_saldo() == 10


@pytest.mark.parametrize("cantidad", [0, -1, "2", None])
def test_consumir_cantidad_invalida(cantidad):
    remesa = crear_remesa()

    with pytest.raises(CantidadAConsumirNoPositivaError):
        remesa.consumir(cantidad)


# --- vencimiento y utilizacion ----------------------------------------------

def test_sin_vencimiento_nunca_vence():
    assert crear_remesa().esta_vencida(date(2100, 1, 1)) is False


def test_esta_vencida():
    remesa = crear_remesa(fecha_vencimiento=fecha(10))

    assert remesa.esta_vencida(fecha(10)) is False
    assert remesa.esta_vencida(fecha(11)) is True
    assert remesa.esta_vencida(date.today() + timedelta(days=11)) is True
    assert remesa.esta_vencida(datetime.now() + timedelta(days=11)) is True


def test_fue_recibida_para():
    remesa = crear_remesa(fecha_recepcion=fecha(-5))

    assert remesa.fue_recibida_para(fecha(-6)) is False
    assert remesa.fue_recibida_para(fecha(-5)) is True


def test_es_utilizable():
    remesa = crear_remesa(fecha_recepcion=fecha(-5), fecha_vencimiento=fecha(5))

    assert remesa.es_utilizable(fecha()) is True
    assert remesa.es_utilizable(fecha(-6)) is False
    assert remesa.es_utilizable(fecha(6)) is False


def test_remesa_agotada_no_es_utilizable():
    remesa = crear_remesa(cantidad_recibida=3)
    remesa.consumir(3)

    assert remesa.es_utilizable(fecha()) is False


@pytest.mark.parametrize("valor", ["2026-01-01", None, 5])
def test_fecha_de_consulta_invalida(valor):
    with pytest.raises(FormatoDeFechaInvalidoError):
        crear_remesa().es_utilizable(valor)


def test_clave_fefo_ordena_por_vencimiento_y_deja_sin_vencimiento_al_final():
    sin_vto = crear_remesa(id_remesa=1)
    vence_tarde = crear_remesa(id_remesa=2, fecha_vencimiento=fecha(20))
    vence_pronto = crear_remesa(id_remesa=3, fecha_vencimiento=fecha(5))

    ordenadas = sorted([sin_vto, vence_tarde, vence_pronto], key=lambda r: r.clave_fefo())

    assert [r.obtener_id_remesa() for r in ordenadas] == [3, 2, 1]


def test_clave_fefo_desempata_por_recepcion():
    nueva = crear_remesa(id_remesa=1, fecha_recepcion=fecha(-1), fecha_vencimiento=fecha(10))
    vieja = crear_remesa(id_remesa=2, fecha_recepcion=fecha(-9), fecha_vencimiento=fecha(10))

    ordenadas = sorted([nueva, vieja], key=lambda r: r.clave_fefo())

    assert [r.obtener_id_remesa() for r in ordenadas] == [2, 1]
