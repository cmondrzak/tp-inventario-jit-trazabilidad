from datetime import date, timedelta

import pytest

from proveedor import Proveedor
from material import Material
from pedido import Pedido
from renglon_pedido import Renglon_pedido
from remesa import Remesa
from movimiento_ingreso import Movimiento_ingreso
from movimiento_retiro import Movimiento_retiro
from gerencia import Gerencia


CLASES_CON_IDS = [Proveedor, Material, Pedido, Renglon_pedido, Remesa, Movimiento_ingreso, Movimiento_retiro]


@pytest.fixture(autouse=True)
def reiniciar_ids():
    """Las listas de ids son atributos de clase: se vacian antes de cada test."""
    for clase in CLASES_CON_IDS:
        clase.lista_id = []
    yield
    for clase in CLASES_CON_IDS:
        clase.lista_id = []


def fecha(dias=0):
    """Fecha dd/mm/aaaa relativa a hoy (dias negativos = pasado)."""
    return (date.today() + timedelta(days=dias)).strftime("%d/%m/%Y")


@pytest.fixture
def gerencia():
    """Gerencia con un deposito, un proveedor (1) y dos materiales registrados."""
    g = Gerencia([], {}, {}, {}, {})
    g.crear_deposito({}, {})
    g.registrar_proveedor(1, "Proveedor SA", 5, "contacto@proveedor.com", "11 1234-5678")
    g.registrar_material(1, "aluminio", "kg", 10)
    g.registrar_material(2, "titanio", "kg", 5)
    return g


@pytest.fixture
def gerencia_con_pedido_aceptado(gerencia):
    """Agrega el pedido 1 (renglon 1: aluminio x 20, renglon 2: titanio x 8) ya aceptado."""
    renglones = [Renglon_pedido(1, "aluminio", 20, 100), Renglon_pedido(2, "titanio", 8, 300)]
    gerencia.generar_pedido(1, 1, renglones, 5)
    gerencia.aceptar_pedido(1)
    return gerencia
