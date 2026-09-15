import pytest

from validaciones import Validaciones
from material import Material
from proveedor import Proveedor
from remesa import Remesa
from renglon import Renglon
from renglon_retiro import RenglonRetiro
from deposito import Deposito


@pytest.fixture(autouse=True)
def reset_material_state():
    # Material.materiales es un atributo de CLASE, compartido por todas las
    # instancias. Sin este reset, un id usado en un test queda "ocupado"
    # para los tests siguientes y Material.validarid empieza a rechazarlo
    # como si fuera un duplicado real.
    Material.materiales = []


@pytest.fixture
def deposito_vacio():
    return Deposito(
        id_deposito=1,
        remesas=[],
        retiros=[],
        politicas=None,
        materiales=[],
        proveedores=[],
        movimientos=[],
    )


def crear_remesa(**overrides):
    # Remesa tiene 8 parámetros; este helper arma un set válido por defecto
    # y cada test solo pisa el campo que quiere probar. material y proveedor
    # van en None porque Remesa todavía no valida nada sobre ellos.
    datos = dict(
        id_remesa=1,
        material=None,
        proveedor=None,
        cantidad_recibida=10,
        saldo_disponible=10,
        fecha_recepcion="2026-03-02",
        fecha_vencimiento="2026-03-20",
        precio_unitario=100,
    )
    datos.update(overrides)
    return Remesa(**datos)


# ---------------------------------------------------------------------------
# Validaciones
# ---------------------------------------------------------------------------

def test_es_positivo_valor_positivo_retorna_true():
    assert Validaciones.es_positivo(10) is True


def test_es_positivo_cero_retorna_false():
    assert Validaciones.es_positivo(0) is False


def test_es_positivo_negativo_retorna_false():
    assert Validaciones.es_positivo(-5) is False


def test_es_positivo_none_retorna_false():
    assert Validaciones.es_positivo(None) is False


def test_es_no_vacio_texto_con_contenido_retorna_true():
    assert Validaciones.es_no_vacio("Aluminio") is True


def test_es_no_vacio_string_vacio_retorna_false():
    assert Validaciones.es_no_vacio("") is False


def test_es_no_vacio_solo_espacios_retorna_false():
    assert Validaciones.es_no_vacio("   ") is False


def test_es_no_vacio_none_retorna_false():
    assert Validaciones.es_no_vacio(None) is False


# ---------------------------------------------------------------------------
# Material
# ---------------------------------------------------------------------------

def test_creacion_material_valida():
    material = Material(1, "Aluminio AL-01", "kg", 10)

    assert material.id_material == 1
    assert material.nombre == "Aluminio AL-01"
    assert material.unidad == "kg"
    assert material.punto_reposicion == 10


def test_material_id_duplicado_lanza_error():
    Material(1, "Aluminio AL-01", "kg", 10)

    # Material.validarid hace `raise ValueError` sin mensaje, así que acá
    # no hay texto que matchear (a diferencia de Cliente, donde sí lo hay).
    with pytest.raises(ValueError):
        Material(1, "Otro material", "kg", 5)


def test_material_id_duplicado_no_registra_segundo_material():
    Material(1, "Aluminio AL-01", "kg", 10)
    cantidad_antes = len(Material.materiales)

    with pytest.raises(ValueError):
        Material(1, "Otro material", "kg", 5)

    assert len(Material.materiales) == cantidad_antes


def test_material_nombre_vacio_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Material(1, "", "kg", 10)


def test_material_nombre_solo_espacios_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Material(1, "   ", "kg", 10)


def test_material_nombre_none_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Material(1, None, "kg", 10)


def test_material_punto_reposicion_cero_lanza_error():
    with pytest.raises(ValueError, match="El punto de reposición debe ser mayor que cero"):
        Material(1, "Aluminio AL-01", "kg", 0)


def test_material_punto_reposicion_negativo_lanza_error():
    with pytest.raises(ValueError, match="El punto de reposición debe ser mayor que cero"):
        Material(1, "Aluminio AL-01", "kg", -5)


def test_material_punto_reposicion_none_lanza_error():
    with pytest.raises(ValueError, match="El punto de reposición debe ser mayor que cero"):
        Material(1, "Aluminio AL-01", "kg", None)


def test_material_punto_reposicion_invalido_no_registra_id():
    # El id se agrega al final del __init__: si la validación del punto de
    # reposición falla antes, el id queda libre para reutilizarse.
    with pytest.raises(ValueError):
        Material(1, "Aluminio AL-01", "kg", 0)

    assert 1 not in Material.materiales

    material = Material(1, "Aluminio AL-01", "kg", 10)
    assert material.id_material == 1


# ---------------------------------------------------------------------------
# Proveedor
# ---------------------------------------------------------------------------

def test_creacion_proveedor_valida():
    proveedor = Proveedor(1, "Proveedor SA", 5)

    assert proveedor.id_proveedor == 1
    assert proveedor.nombre == "Proveedor SA"
    assert proveedor.plazo_entrega == 5


def test_proveedor_nombre_vacio_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Proveedor(1, "", 5)


def test_proveedor_nombre_solo_espacios_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Proveedor(1, "   ", 5)


def test_proveedor_nombre_none_lanza_error():
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        Proveedor(1, None, 5)


def test_proveedor_plazo_entrega_cero_lanza_error():
    with pytest.raises(ValueError, match="El plazo de entrega debe ser mayor que cero"):
        Proveedor(1, "Proveedor SA", 0)


def test_proveedor_plazo_entrega_negativo_lanza_error():
    with pytest.raises(ValueError, match="El plazo de entrega debe ser mayor que cero"):
        Proveedor(1, "Proveedor SA", -1)


def test_proveedor_plazo_entrega_none_lanza_error():
    with pytest.raises(ValueError, match="El plazo de entrega debe ser mayor que cero"):
        Proveedor(1, "Proveedor SA", None)


# ---------------------------------------------------------------------------
# Remesa
# ---------------------------------------------------------------------------

def test_creacion_remesa_valida():
    remesa = crear_remesa()

    assert remesa.cantidad_recibida == 10
    assert remesa.saldo_disponible == 10
    assert remesa.precio_unitario == 100


def test_remesa_cantidad_recibida_cero_lanza_error():
    with pytest.raises(ValueError, match="La cantidad recibida debe ser mayor que cero"):
        crear_remesa(cantidad_recibida=0)


def test_remesa_cantidad_recibida_negativa_lanza_error():
    with pytest.raises(ValueError, match="La cantidad recibida debe ser mayor que cero"):
        crear_remesa(cantidad_recibida=-5)


def test_remesa_cantidad_recibida_none_lanza_error():
    with pytest.raises(ValueError, match="La cantidad recibida debe ser mayor que cero"):
        crear_remesa(cantidad_recibida=None)


def test_remesa_precio_unitario_cero_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        crear_remesa(precio_unitario=0)


def test_remesa_precio_unitario_negativo_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        crear_remesa(precio_unitario=-1)


def test_remesa_precio_unitario_none_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        crear_remesa(precio_unitario=None)


def test_remesa_sin_fecha_vencimiento_no_lanza_error():
    # RN13: una remesa puede no tener fecha de vencimiento. A diferencia de
    # cantidad_recibida o precio_unitario, acá None es un valor válido.
    remesa = crear_remesa(fecha_vencimiento=None)

    assert remesa.fecha_vencimiento is None


# ---------------------------------------------------------------------------
# Renglon
# ---------------------------------------------------------------------------

def test_creacion_renglon_valida_y_subtotal():
    renglon = Renglon(material=None, cantidad=3, precio_unitario=50)

    assert renglon.subtotal_renglon() == 150


def test_renglon_cantidad_cero_lanza_error():
    with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
        Renglon(material=None, cantidad=0, precio_unitario=50)


def test_renglon_cantidad_negativa_lanza_error():
    with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
        Renglon(material=None, cantidad=-1, precio_unitario=50)


def test_renglon_cantidad_none_lanza_error():
    with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
        Renglon(material=None, cantidad=None, precio_unitario=50)


def test_renglon_precio_unitario_cero_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        Renglon(material=None, cantidad=3, precio_unitario=0)


def test_renglon_precio_unitario_negativo_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        Renglon(material=None, cantidad=3, precio_unitario=-1)


def test_renglon_precio_unitario_none_lanza_error():
    with pytest.raises(ValueError, match="El precio unitario debe ser mayor que cero"):
        Renglon(material=None, cantidad=3, precio_unitario=None)


# ---------------------------------------------------------------------------
# RenglonRetiro
# ---------------------------------------------------------------------------

def test_creacion_renglon_retiro_valida():
    renglon_retiro = RenglonRetiro(material=None, remesa_modificada=None, cantidad_solicitada=5)

    assert renglon_retiro.cantidad_solicitada == 5


def test_renglon_retiro_cantidad_solicitada_cero_lanza_error():
    with pytest.raises(ValueError, match="La cantidad solicitada debe ser mayor que cero"):
        RenglonRetiro(material=None, remesa_modificada=None, cantidad_solicitada=0)


def test_renglon_retiro_cantidad_solicitada_negativa_lanza_error():
    with pytest.raises(ValueError, match="La cantidad solicitada debe ser mayor que cero"):
        RenglonRetiro(material=None, remesa_modificada=None, cantidad_solicitada=-3)


def test_renglon_retiro_cantidad_solicitada_none_lanza_error():
    with pytest.raises(ValueError, match="La cantidad solicitada debe ser mayor que cero"):
        RenglonRetiro(material=None, remesa_modificada=None, cantidad_solicitada=None)


# ---------------------------------------------------------------------------
# Deposito.generar_retiro
# ---------------------------------------------------------------------------
# generar_retiro solo valida hoy que la cantidad solicitada sea positiva y
# después hace `return` (FEFO y existencia disponible todavía no están
# implementados). Por eso estos tests se limitan a esa validación de guardia.

def test_deposito_generar_retiro_cantidad_cero_lanza_error(deposito_vacio):
    with pytest.raises(ValueError, match="La cantidad a retirar debe ser mayor que cero"):
        deposito_vacio.generar_retiro(0)


def test_deposito_generar_retiro_cantidad_negativa_lanza_error(deposito_vacio):
    with pytest.raises(ValueError, match="La cantidad a retirar debe ser mayor que cero"):
        deposito_vacio.generar_retiro(-10)


def test_deposito_generar_retiro_cantidad_none_lanza_error(deposito_vacio):
    with pytest.raises(ValueError, match="La cantidad a retirar debe ser mayor que cero"):
        deposito_vacio.generar_retiro(None)


def test_deposito_generar_retiro_cantidad_valida_no_lanza_error(deposito_vacio):
    deposito_vacio.generar_retiro(10)  # no debe lanzar excepción


# ---------------------------------------------------------------------------
# Deposito.registrar_material
# ---------------------------------------------------------------------------
# registrar_material delega la validación en Material, así que estos son en
# el fondo tests de integración: confirman que Deposito deja propagar las
# excepciones de Material en vez de tragárselas.

def test_deposito_registrar_material_valido_lo_agrega_a_la_lista(deposito_vacio):
    deposito_vacio.registrar_material(1, "Aluminio AL-01", "kg", 10)

    assert len(deposito_vacio.materiales) == 1
    assert deposito_vacio.materiales[0].id_material == 1


def test_deposito_registrar_material_id_duplicado_lanza_error(deposito_vacio):
    deposito_vacio.registrar_material(1, "Aluminio AL-01", "kg", 10)

    with pytest.raises(ValueError):
        deposito_vacio.registrar_material(1, "Otro material", "kg", 5)


def test_deposito_registrar_material_invalido_no_lo_agrega_a_la_lista(deposito_vacio):
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        deposito_vacio.registrar_material(1, "", "kg", 10)

    assert deposito_vacio.materiales == []