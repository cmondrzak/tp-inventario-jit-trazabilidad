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
def gerencia():
    g = Gerencia()
    g.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    g.registrar_proveedor("P1", "Proveedor SA", "contacto@proveedor.com", "12345678")
    return g


# ---------------------------------------------------------------------------
# Materiales y proveedores
# ---------------------------------------------------------------------------

def test_registrar_material_lo_deja_disponible_por_id(gerencia):
    assert gerencia.materiales["AL-01"].nombre == "Aluminio AL-01"


def test_registrar_material_id_duplicado_lanza_error(gerencia):
    with pytest.raises(IdentificadorDuplicadoError):
        gerencia.registrar_material("AL-01", "Otro", "kg", 5)


def test_registrar_material_invalido_no_queda_registrado(gerencia):
    with pytest.raises(Exception):
        gerencia.registrar_material("AL-02", "", "kg", 10)
    assert "AL-02" not in gerencia.materiales


def test_registrar_proveedor_id_duplicado_lanza_error(gerencia):
    with pytest.raises(IdentificadorDuplicadoError):
        gerencia.registrar_proveedor("P1", "Otro", "otro@mail.com", "12345678")


def test_obtener_material_inexistente_lanza_error(gerencia):
    with pytest.raises(MaterialNoEncontradoError):
        gerencia.obtener_material("NO-EXISTE")


def test_obtener_proveedor_inexistente_lanza_error(gerencia):
    with pytest.raises(ProveedorNoEncontradoError):
        gerencia.obtener_proveedor("NO-EXISTE")