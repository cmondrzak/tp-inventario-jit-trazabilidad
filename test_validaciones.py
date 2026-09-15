"""
Tests de las VALIDACIONES del sistema (RN1, RN3, RN5, RN9, RN18 parcial, etc).

Alcance de este archivo:
- Se prueban únicamente las validaciones que ya están implementadas en los
  constructores (las que llaman a Validaciones.es_positivo / es_no_vacio) y
  la verificación de guardia en Deposito.generar_retiro.
- NO se prueban comportamientos como FEFO, existencia disponible, trazabilidad
  de movimientos, etc., porque esos métodos todavía devuelven `return` (no
  están implementados). Cuando los implementes, esos casos van en otro
  archivo (por ejemplo test_deposito_retiros.py) para no mezclar
  responsabilidades.

Cómo correrlo:
    pytest -v
"""

import pytest

from validaciones import Validaciones
from material import Material
from proveedor import Proveedor
from remesa import Remesa
from renglon import Renglon
from renglon_retiro import RenglonRetiro
from deposito import Deposito


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def limpiar_registro_materiales():
    """
    Material guarda los ids ya usados en un atributo DE CLASE (Material.materiales),
    compartido por todas las instancias. Si no lo reseteamos, un test que crea
    un Material con id=1 "contamina" a los tests siguientes y Material.validarid
    empieza a tirar ValueError por duplicado aunque el test no tenga nada que
    ver con duplicados.

    autouse=True hace que este fixture se ejecute solo, antes de CADA test,
    sin que haya que pedirlo explícitamente como parámetro.
    """
    Material.materiales.clear()
    yield
    Material.materiales.clear()


@pytest.fixture
def deposito_vacio():
    """Depósito con todas sus colecciones vacías, listo para registrar cosas."""
    return Deposito(
        id_deposito=1,
        remesas=[],
        retiros=[],
        politicas=None,
        materiales=[],
        proveedores=[],
        movimientos=[],
    )


# ---------------------------------------------------------------------------
# Validaciones (funciones puras, sin dependencias de otras clases)
# ---------------------------------------------------------------------------

class TestEsPositivo:
    """
    Estas son pruebas unitarias "puras": no involucran ninguna otra clase,
    solo la función es_positivo. Las escribo primero y por separado porque
    es la base sobre la que se apoyan todas las demás validaciones: si esta
    función tuviera un bug, fallaría en cascada en Material, Remesa, Renglon,
    etc. Aislarla permite detectar el problema en el lugar exacto.
    """

    @pytest.mark.parametrize("valor", [1, 0.5, 10, 100_000])
    def test_valores_positivos_retornan_true(self, valor):
        assert Validaciones.es_positivo(valor) is True

    @pytest.mark.parametrize("valor", [0, -1, -0.01, -100])
    def test_cero_y_negativos_retornan_false(self, valor):
        # Caso borde importante: 0 NO es positivo. Lo pruebo explícitamente
        # y por separado de los negativos porque es el error "off-by-one"
        # más común (usar >= en vez de > en la implementación).
        assert Validaciones.es_positivo(valor) is False

    def test_none_retorna_false(self):
        # None no debería explotar con una excepción (TypeError al comparar
        # None > 0); la validación tiene que "atajarlo" y devolver False.
        assert Validaciones.es_positivo(None) is False


class TestEsNoVacio:

    @pytest.mark.parametrize("texto", ["Aluminio", "a", "  texto con espacios  "])
    def test_texto_con_contenido_retorna_true(self, texto):
        assert Validaciones.es_no_vacio(texto) is True

    @pytest.mark.parametrize("texto", ["", "   ", "\t", "\n"])
    def test_string_vacio_o_solo_espacios_retorna_false(self, texto):
        # "   ".strip() == "" -> por eso un string de solo espacios también
        # se considera vacío. Es un caso borde que vale la pena dejar explícito.
        assert Validaciones.es_no_vacio(texto) is False

    def test_none_retorna_false(self):
        assert Validaciones.es_no_vacio(None) is False


# ---------------------------------------------------------------------------
# Material (RN1: id único, RN2/RN3: nombre y punto de reposición)
# ---------------------------------------------------------------------------

class TestMaterial:

    def test_creacion_valida(self):
        m = Material(1, "Aluminio AL-01", "kg", 10)
        assert m.id_material == 1
        assert m.nombre == "Aluminio AL-01"
        assert m.punto_reposicion == 10

    def test_id_duplicado_lanza_value_error(self):
        # RN1: identificador único dentro del sistema.
        Material(1, "Aluminio AL-01", "kg", 10)
        with pytest.raises(ValueError):
            Material(1, "Otro material", "kg", 5)

    def test_id_duplicado_no_agrega_el_segundo_material_al_registro(self):
        # Además de que explote, verificamos que no queden "restos" del
        # intento fallido: el registro de ids no debería crecer con un id
        # que ya rechazamos.
        Material(1, "Aluminio AL-01", "kg", 10)
        cantidad_antes = len(Material.materiales)
        with pytest.raises(ValueError):
            Material(1, "Otro material", "kg", 5)
        assert len(Material.materiales) == cantidad_antes

    @pytest.mark.parametrize("nombre_invalido", ["", "   ", None])
    def test_nombre_invalido_lanza_value_error(self, nombre_invalido):
        # RN2: el nombre es obligatorio.
        with pytest.raises(ValueError):
            Material(1, nombre_invalido, "kg", 10)

    @pytest.mark.parametrize("punto_reposicion_invalido", [0, -5, None])
    def test_punto_reposicion_invalido_lanza_value_error(self, punto_reposicion_invalido):
        # RN3: el punto de reposición debe ser mayor que cero.
        with pytest.raises(ValueError):
            Material(1, "Aluminio AL-01", "kg", punto_reposicion_invalido)

    def test_punto_reposicion_invalido_no_registra_el_id(self):
        # Efecto colateral a vigilar: si falla la validación del punto de
        # reposición, el id NO debería quedar registrado, porque
        # Material.materiales.append(id_material) es la última línea del
        # __init__. Si el ValueError se dispara antes, nunca se llega a
        # ejecutar ese append, así que el id queda libre para reutilizarse.
        with pytest.raises(ValueError):
            Material(1, "Aluminio AL-01", "kg", 0)
        assert 1 not in Material.materiales
        # Y como prueba de que quedó libre, ahora sí debería poder crearse:
        m = Material(1, "Aluminio AL-01", "kg", 10)
        assert m.id_material == 1


# ---------------------------------------------------------------------------
# Proveedor (RN5: nombre y plazo de entrega)
# ---------------------------------------------------------------------------

class TestProveedor:

    def test_creacion_valida(self):
        p = Proveedor(1, "Proveedor SA", 5)
        assert p.id_proveedor == 1
        assert p.nombre == "Proveedor SA"
        assert p.plazo_entrega == 5

    @pytest.mark.parametrize("nombre_invalido", ["", "   ", None])
    def test_nombre_invalido_lanza_value_error(self, nombre_invalido):
        with pytest.raises(ValueError):
            Proveedor(1, nombre_invalido, 5)

    @pytest.mark.parametrize("plazo_invalido", [0, -1, None])
    def test_plazo_entrega_invalido_lanza_value_error(self, plazo_invalido):
        with pytest.raises(ValueError):
            Proveedor(1, "Proveedor SA", plazo_invalido)

    # Nota: a diferencia de Material, esta clase NO valida id duplicado
    # dentro de su propio __init__ (no tiene un Proveedor.proveedores como
    # registro de clase). La RN4 ("identificador único") queda, por ahora,
    # sin implementar acá — se las marco como pendiente más abajo en mi
    # explicación, no la doy por hecha en un test que fallaría.


# ---------------------------------------------------------------------------
# Remesa (RN9: cantidad recibida > 0, precio unitario > 0)
# ---------------------------------------------------------------------------

class TestRemesa:

    def _crear_remesa(self, **overrides):
        """
        Helper para no repetir los 8 argumentos posicionales en cada test.
        material y proveedor los paso como None porque, para estas pruebas
        de validación puntual, no importa qué objeto sea: Remesa no valida
        nada sobre ellos todavía.
        """
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

    def test_creacion_valida(self):
        r = self._crear_remesa()
        assert r.cantidad_recibida == 10
        assert r.precio_unitario == 100

    @pytest.mark.parametrize("cantidad_invalida", [0, -5, None])
    def test_cantidad_recibida_invalida_lanza_value_error(self, cantidad_invalida):
        with pytest.raises(ValueError):
            self._crear_remesa(cantidad_recibida=cantidad_invalida)

    @pytest.mark.parametrize("precio_invalido", [0, -1, None])
    def test_precio_unitario_invalido_lanza_value_error(self, precio_invalido):
        with pytest.raises(ValueError):
            self._crear_remesa(precio_unitario=precio_invalido)

    def test_remesa_sin_fecha_vencimiento_no_lanza_error(self):
        # RN13: una remesa puede no tener fecha de vencimiento. Este test
        # documenta que None es un valor válido para ese campo puntual
        # (distinto de cantidad_recibida o precio_unitario, donde None
        # SÍ debe rechazarse).
        r = self._crear_remesa(fecha_vencimiento=None)
        assert r.fecha_vencimiento is None


# ---------------------------------------------------------------------------
# Renglon (RN31/RN32: cantidad y precio unitario > 0)
# ---------------------------------------------------------------------------

class TestRenglon:

    def test_creacion_valida_y_subtotal(self):
        r = Renglon(material=None, cantidad=3, precio_unitario=50)
        assert r.subtotal_renglon() == 150

    @pytest.mark.parametrize("cantidad_invalida", [0, -1, None])
    def test_cantidad_invalida_lanza_value_error(self, cantidad_invalida):
        with pytest.raises(ValueError):
            Renglon(material=None, cantidad=cantidad_invalida, precio_unitario=50)

    @pytest.mark.parametrize("precio_invalido", [0, -1, None])
    def test_precio_unitario_invalido_lanza_value_error(self, precio_invalido):
        with pytest.raises(ValueError):
            Renglon(material=None, cantidad=3, precio_unitario=precio_invalido)


# ---------------------------------------------------------------------------
# RenglonRetiro
# ---------------------------------------------------------------------------

class TestRenglonRetiro:

    def test_creacion_valida(self):
        rr = RenglonRetiro(material=None, remesa_modificada=None, cantidad_solicitada=5)
        assert rr.cantidad_solicitada == 5

    @pytest.mark.parametrize("cantidad_invalida", [0, -3, None])
    def test_cantidad_solicitada_invalida_lanza_value_error(self, cantidad_invalida):
        with pytest.raises(ValueError):
            RenglonRetiro(material=None, remesa_modificada=None,
                          cantidad_solicitada=cantidad_invalida)


# ---------------------------------------------------------------------------
# Deposito.generar_retiro (validación de guardia, RN18 parcial)
# ---------------------------------------------------------------------------

class TestDepositoGenerarRetiro:
    """
    Importante: generar_retiro hoy SOLO valida que la cantidad solicitada
    sea positiva y después hace `return` (sin implementar FEFO ni
    existencia disponible todavía). Por eso estos tests se limitan a esa
    validación de guardia y no verifican nada sobre remesas consumidas:
    eso vendría en tests de integración separados una vez que el método
    esté implementado, siguiendo RN18-RN22.
    """

    @pytest.mark.parametrize("cantidad_invalida", [0, -10, None])
    def test_cantidad_solicitada_invalida_lanza_value_error(self, deposito_vacio, cantidad_invalida):
        with pytest.raises(ValueError):
            deposito_vacio.generar_retiro(cantidad_invalida)

    def test_cantidad_solicitada_valida_no_lanza_error(self, deposito_vacio):
        # No verificamos el valor de retorno porque el método todavía no
        # está implementado (retorna None). Solo confirmamos que la
        # validación de guardia no bloquea un caso correcto.
        deposito_vacio.generar_retiro(10)  # no debe lanzar excepción


class TestDepositoRegistrarMaterial:
    """
    registrar_material delega la validación en Material (RN1, RN3), así que
    estos tests son en el fondo tests de integración: confirman que
    Deposito no "traga" ni ignora las excepciones que Material lanza, sino
    que las deja propagarse hacia el código cliente.
    """

    def test_registrar_material_valido_lo_agrega_a_la_lista(self, deposito_vacio):
        deposito_vacio.registrar_material(1, "Aluminio AL-01", "kg", 10)
        assert len(deposito_vacio.materiales) == 1
        assert deposito_vacio.materiales[0].id_material == 1

    def test_registrar_material_con_id_duplicado_lanza_value_error(self, deposito_vacio):
        deposito_vacio.registrar_material(1, "Aluminio AL-01", "kg", 10)
        with pytest.raises(ValueError):
            deposito_vacio.registrar_material(1, "Otro material", "kg", 5)

    def test_registrar_material_invalido_no_lo_agrega_a_la_lista(self, deposito_vacio):
        # Si Material() lanza la excepción, la línea
        # self.materiales.append(m) nunca se ejecuta -> la lista del
        # depósito debe seguir vacía.
        with pytest.raises(ValueError):
            deposito_vacio.registrar_material(1, "", "kg", 10)
        assert deposito_vacio.materiales == []
