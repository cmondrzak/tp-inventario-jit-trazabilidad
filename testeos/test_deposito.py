from datetime import date

import pytest

from deposito import Deposito
from gerencia import Gerencia
from exceptions import (
    CantidadInvalidaError,
    ExistenciaInsuficienteError,
    IdentificadorDuplicadoError,
    MaterialNoEncontradoError,
    ProveedorNoEncontradoError,
)


@pytest.fixture
def deposito():
    d = Deposito()
    d.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    d.registrar_proveedor("P1", "Proveedor SA", "contacto@proveedor.com", "12345678")
    return d


# ---------------------------------------------------------------------------
# Materiales y proveedores
# ---------------------------------------------------------------------------

def test_registrar_material_lo_deja_disponible_por_id(deposito):
    assert deposito.materiales["AL-01"].nombre == "Aluminio AL-01"


def test_registrar_material_id_duplicado_lanza_error(deposito):
    with pytest.raises(IdentificadorDuplicadoError):
        deposito.registrar_material("AL-01", "Otro", "kg", 5)


def test_registrar_material_invalido_no_queda_registrado(deposito):
    with pytest.raises(Exception):
        deposito.registrar_material("AL-02", "", "kg", 10)
    assert "AL-02" not in deposito.materiales


def test_registrar_proveedor_id_duplicado_lanza_error(deposito):
    with pytest.raises(IdentificadorDuplicadoError):
        deposito.registrar_proveedor("P1", "Otro", "otro@mail.com", "12345678")


def test_obtener_material_inexistente_lanza_error(deposito):
    with pytest.raises(MaterialNoEncontradoError):
        deposito.obtener_material("NO-EXISTE")


def test_obtener_proveedor_inexistente_lanza_error(deposito):
    with pytest.raises(ProveedorNoEncontradoError):
        deposito.obtener_proveedor("NO-EXISTE")


# ---------------------------------------------------------------------------
# crear_remesa: la consigna de **kwargs, de punta a punta
# ---------------------------------------------------------------------------

def test_crear_remesa_valida_queda_registrada_con_saldo_igual_a_cantidad(deposito):
    remesa = deposito.crear_remesa("R-1", "AL-01", "P1", 10,
                                    fecha_recepcion=date(2026, 3, 2))

    assert deposito.remesas["R-1"] is remesa
    assert remesa.saldo_disponible == 10  # RN12


def test_crear_remesa_id_duplicado_lanza_error(deposito):
    deposito.crear_remesa("R-1", "AL-01", "P1", 10)
    with pytest.raises(IdentificadorDuplicadoError):
        deposito.crear_remesa("R-1", "AL-01", "P1", 5)


def test_crear_remesa_material_inexistente_lanza_error(deposito):
    with pytest.raises(MaterialNoEncontradoError):
        deposito.crear_remesa("R-1", "NO-EXISTE", "P1", 10)


def test_crear_remesa_proveedor_inexistente_lanza_error(deposito):
    with pytest.raises(ProveedorNoEncontradoError):
        deposito.crear_remesa("R-1", "AL-01", "NO-EXISTE", 10)


def test_crear_remesa_cantidad_invalida_lanza_error(deposito):
    with pytest.raises(CantidadInvalidaError):
        deposito.crear_remesa("R-1", "AL-01", "P1", 0)


def test_crear_remesa_sin_fecha_vencimiento_es_valida(deposito):
    # RN13
    remesa = deposito.crear_remesa("R-1", "AL-01", "P1", 10)
    assert remesa.fecha_vencimiento is None


def test_crear_remesa_con_fecha_vencimiento_por_kwargs(deposito):
    remesa = deposito.crear_remesa("R-1", "AL-01", "P1", 10,
                                    fecha_vencimiento=date(2026, 3, 20))
    assert remesa.fecha_vencimiento == date(2026, 3, 20)


def test_crear_remesa_datos_opcionales_no_previstos_no_rompen_la_firma(deposito):
    # Este es el punto central de la consigna: agregar un dato nuevo
    # (lote_proveedor) no obliga a tocar crear_remesa ni Remesa.
    remesa = deposito.crear_remesa(
        "R-1", "AL-01", "P1", 10,
        fecha_vencimiento=date(2026, 3, 20),
        lote_proveedor="L-998",
        nro_guia="G-123",
    )
    assert remesa.obtener_dato("lote_proveedor") == "L-998"
    assert remesa.obtener_dato("nro_guia") == "G-123"


def test_crear_remesa_registra_movimiento_de_ingreso(deposito):
    # RN23
    assert deposito.movimientos == []
    deposito.crear_remesa("R-1", "AL-01", "P1", 10)
    assert len(deposito.movimientos) == 1
    assert deposito.movimientos[0].remesa.id_remesa == "R-1"


# ---------------------------------------------------------------------------
# Existencias (RN15-RN17)
# ---------------------------------------------------------------------------

def _cargar_escenario_readme(deposito):
    deposito.crear_remesa("R-101", "AL-01", "P1", 8,
                           fecha_recepcion=date(2026, 3, 2),
                           fecha_vencimiento=date(2026, 3, 20))
    deposito.crear_remesa("R-102", "AL-01", "P1", 12,
                           fecha_recepcion=date(2026, 3, 4),
                           fecha_vencimiento=date(2026, 3, 30))
    deposito.crear_remesa("R-103", "AL-01", "P1", 15,
                           fecha_recepcion=date(2026, 3, 5))
    return deposito


def test_existencia_fisica_suma_todos_los_saldos_sin_importar_vencimiento(deposito):
    _cargar_escenario_readme(deposito)
    assert deposito.existencia_fisica("AL-01") == 35


def test_existencia_disponible_excluye_vencidas(deposito):
    _cargar_escenario_readme(deposito)
    # al 05/04, R-101 (vence 20/03) y R-102 (vence 30/03) están vencidas;
    # solo R-103 (sin vencimiento) sigue disponible.
    assert deposito.existencia_disponible("AL-01", date(2026, 4, 5)) == 15


def test_existencia_disponible_excluye_remesas_sin_saldo(deposito):
    d = _cargar_escenario_readme(deposito)
    d.generar_retiro("AL-01", 8, date(2026, 3, 10))  # agota R-101 vía FEFO
    assert d.existencia_disponible("AL-01", date(2026, 3, 10)) == 12 + 15


# ---------------------------------------------------------------------------
# Retiros (RN18-RN22) y FEFO end-to-end
# ---------------------------------------------------------------------------

def test_retiro_con_una_sola_remesa_alcanza(deposito):
    deposito.crear_remesa("R-1", "AL-01", "P1", 10, fecha_vencimiento=date(2026, 5, 1))
    movimientos = deposito.generar_retiro("AL-01", 4, date(2026, 3, 1))

    assert len(movimientos) == 1
    assert deposito.remesas["R-1"].saldo_disponible == 6


def test_retiro_distribuye_el_consumo_entre_varias_remesas_respetando_fefo(deposito):
    _cargar_escenario_readme(deposito)

    movimientos = deposito.generar_retiro("AL-01", 18, date(2026, 3, 10))

    ids_consumidos = [m.renglon_retiro.remesa.id_remesa for m in movimientos]
    assert ids_consumidos == ["R-101", "R-102"]  # FEFO: vence antes primero
    assert deposito.remesas["R-101"].saldo_disponible == 0
    assert deposito.remesas["R-102"].saldo_disponible == 2
    assert deposito.remesas["R-103"].saldo_disponible == 15  # no tocada


def test_retiro_cantidad_no_positiva_lanza_error(deposito):
    with pytest.raises(CantidadInvalidaError):
        deposito.generar_retiro("AL-01", 0, date(2026, 3, 1))


def test_retiro_supera_existencia_disponible_lanza_error(deposito):
    deposito.crear_remesa("R-1", "AL-01", "P1", 10)
    with pytest.raises(ExistenciaInsuficienteError):
        deposito.generar_retiro("AL-01", 11, date(2026, 3, 1))


def test_retiro_rechazado_no_modifica_el_inventario(deposito):
    # RN22, tercer escenario del README.
    _cargar_escenario_readme(deposito)
    fecha = date(2026, 4, 5)
    deposito.generar_retiro("AL-01", 5, fecha)  # consume R-103 (único utilizable)

    disponible_antes = deposito.existencia_disponible("AL-01", fecha)
    saldo_r103_antes = deposito.remesas["R-103"].saldo_disponible

    with pytest.raises(ExistenciaInsuficienteError):
        deposito.generar_retiro("AL-01", 20, fecha)

    assert deposito.existencia_disponible("AL-01", fecha) == disponible_antes
    assert deposito.remesas["R-103"].saldo_disponible == saldo_r103_antes
    # R-101 y R-102 ya estaban vencidas y con su saldo original: el
    # intento de retiro rechazado no debe haberlas tocado tampoco.
    assert deposito.remesas["R-101"].saldo_disponible == 8
    assert deposito.remesas["R-102"].saldo_disponible == 12


def test_retiro_actualiza_saldos_correctamente_escenario_readme(deposito):
    _cargar_escenario_readme(deposito)
    deposito.generar_retiro("AL-01", 18, date(2026, 3, 10))

    assert deposito.existencia_fisica("AL-01") == 17
    assert deposito.existencia_disponible("AL-01", date(2026, 3, 10)) == 17


# ---------------------------------------------------------------------------
# Trazabilidad (RN23-RN26)
# ---------------------------------------------------------------------------

def test_retiro_genera_un_movimiento_por_cada_remesa_consumida(deposito):
    _cargar_escenario_readme(deposito)
    movimientos = deposito.generar_retiro("AL-01", 18, date(2026, 3, 10))
    assert len(movimientos) == 2  # RN24: R-101 y R-102


def test_remesas_de_retiro_reconstruye_las_remesas_involucradas(deposito):
    _cargar_escenario_readme(deposito)
    movimientos = deposito.generar_retiro("AL-01", 18, date(2026, 3, 10))
    id_movimiento = movimientos[0].id_movimiento

    remesas = deposito.remesas_de_retiro(id_movimiento)
    assert [r.id_remesa for r in remesas] == ["R-101"]


def test_retiros_de_remesa_reconstruye_los_retiros_en_que_participo(deposito):
    _cargar_escenario_readme(deposito)
    movimientos = deposito.generar_retiro("AL-01", 18, date(2026, 3, 10))
    ids_esperados = [m.id_movimiento for m in movimientos]

    assert deposito.retiros_de_remesa("R-101") == [ids_esperados[0]]
    assert deposito.retiros_de_remesa("R-102") == [ids_esperados[1]]
    assert deposito.retiros_de_remesa("R-103") == []  # no participó


# ---------------------------------------------------------------------------
# Reposición (RN27-RN28)
# ---------------------------------------------------------------------------

def test_requiere_reposicion_cuando_disponible_cae_debajo_del_punto(deposito):
    deposito.crear_remesa("R-1", "AL-01", "P1", 12)  # punto_reposicion = 10
    deposito.generar_retiro("AL-01", 5, date(2026, 3, 1))  # queda en 7

    assert deposito.requiere_reposicion("AL-01", date(2026, 3, 1)) is True


def test_no_requiere_reposicion_si_disponible_iguala_el_punto(deposito):
    deposito.crear_remesa("R-1", "AL-01", "P1", 10)  # punto_reposicion = 10
    assert deposito.requiere_reposicion("AL-01", date(2026, 3, 1)) is False


def test_reposicion_usa_disponible_no_fisica(deposito):
    # Escenario clásico: hay stock físico (una remesa vencida) pero
    # nada disponible -> igual debería marcar reposición si lo
    # disponible < punto (acá disponible = 0 < 10).
    deposito.crear_remesa("R-1", "AL-01", "P1", 20,
                           fecha_vencimiento=date(2026, 1, 1))  # ya vencida
    fecha_operacion = date(2026, 2, 1)

    assert deposito.existencia_fisica("AL-01") == 20
    assert deposito.existencia_disponible("AL-01", fecha_operacion) == 0
    assert deposito.requiere_reposicion("AL-01", fecha_operacion) is True


# ---------------------------------------------------------------------------
# A través de Gerencia (fachada)
# ---------------------------------------------------------------------------

def test_gerencia_delega_correctamente_en_deposito():
    deposito = Deposito()
    gerencia = Gerencia(deposito)

    gerencia.registrar_material("AL-01", "Aluminio", "kg", 10)
    gerencia.registrar_proveedor("P1", "Proveedor SA", "c@p.com", "12345678")
    gerencia.crear_remesa("R-1", "AL-01", "P1", 10)

    assert gerencia.existencia_fisica("AL-01") == 10


def test_gerencia_generar_pedido_y_calcular_subtotal():
    deposito = Deposito()
    gerencia = Gerencia(deposito)
    gerencia.registrar_proveedor("P1", "Proveedor SA", "c@p.com", "12345678")

    pedido = gerencia.generar_pedido("PED-1", "P1", plazo_entrega=7)

    from renglon_pedido import RenglonPedido
    pedido.generar_renglon(RenglonPedido(1, "AL-01", 20, 150))

    assert pedido.subtotal_pedido() == 3000
    assert gerencia.obtener_pedidos()["PED-1"] is pedido